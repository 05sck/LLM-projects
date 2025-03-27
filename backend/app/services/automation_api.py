# backend/app/services/automation_api.py
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

import google.generativeai as genai  # Gemini 추가
import mysql.connector
import numpy as np
import pandas as pd
import requests
from app.config.mysql_config import config as db_config
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
WEATHER_API_SERVICE_KEY = os.getenv("WEATHER_API_SERVICE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Gemini API 키가 설정되지 않았습니다.")
print("API 키가 정상적으로 로드되었습니다!")

# Gemini 설정
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

BASE_DIR = Path(__file__).resolve().parent

def extract_float(s):
    numbers = re.findall(r'[-]?\d+\.\d+|[-]?\d+', s)
    return float(numbers[0]) if numbers else 0

class WeatherActivityAdvisor:
    def __init__(self, service_key):
        self.service_key = service_key
        self.weather_data = None
        self.base_url_weather = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"
        self.base_date = datetime.now().strftime("%Y%m%d")

    def get_weather_forecast_by_date(self, nx, ny):
        now = datetime.now()
        if now.hour < 2:
            base_date = (now - timedelta(days=1)).strftime("%Y%m%d")
            base_time = "2300"
        elif now.hour < 5:
            base_time = "0200"
        elif now.hour < 8:
            base_time = "0500"
        elif now.hour < 11:
            base_time = "0800"
        elif now.hour < 14:
            base_time = "1100"
        elif now.hour < 17:
            base_time = "1400"
        elif now.hour < 20:
            base_time = "1700"
        elif now.hour < 23:
            base_time = "2000"
        else:
            base_time = "2300"

        url = f"{self.base_url_weather}/getVilageFcst"
        params = {
            'serviceKey': self.service_key,
            'pageNo': '1',
            'numOfRows': '1000',
            'dataType': 'JSON',
            'base_date': self.base_date,
            'base_time': base_time,
            'nx': nx,
            'ny': ny
        }
        response = requests.get(url, params=params)
        print(f"기상청 응답: {response.status_code} - {response.text[:200]}")
        if response.status_code == 200:
            if "<OpenAPI_ServiceResponse>" in response.text:
                root = ET.fromstring(response.text)
                err_msg = root.find(".//errMsg").text
                return_auth_msg = root.find(".//returnAuthMsg").text
                raise Exception(f"기상청 API 에러: {err_msg} - {return_auth_msg}")
            data = response.json()
            print(f"기상청 데이터: {len(data['response']['body']['items']['item'])} 항목 가져옴")
            items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
            self.weather_data = pd.DataFrame(items)
        else:
            raise Exception(f"기상청 API 실패: {response.status_code}")
        return self.weather_data

    def process_weather_data(self):
        df = self.weather_data
        df = df.pivot(index=['baseDate', "fcstDate", 'fcstTime', 'nx', 'ny', 'baseTime'], columns='category', values='fcstValue').reset_index()
        df.insert(0, 'datefcst', pd.to_datetime(df['fcstDate'].astype(str) + df['fcstTime'].str.zfill(4), format='%Y%m%d%H%M'))
        df.insert(0, 'datenow', pd.to_datetime(df['baseDate'].astype(str) + df['baseTime'].str.zfill(4), format='%Y%m%d%H%M'))
        df['PCP'] = df['PCP'].replace('강수없음', 0)
        df['SNO'] = df['SNO'].replace('적설없음', 0)
        df['PCP'] = df['PCP'].astype(str).apply(extract_float)
        df.drop(columns=['baseDate', 'baseTime', 'fcstDate', 'fcstTime', 'WAV', 'UUU', 'TMN', 'TMX', 'VEC', 'VVV'], inplace=True)
        self.weather_data = df
        df.to_csv(BASE_DIR / 'weather_data_refined.csv', index=False)
        return df

    def decision_making(self):
        df_weather = pd.read_csv(BASE_DIR / 'weather_data_refined.csv')
        print(f"날씨 데이터 행 수: {len(df_weather)}")
        df_rule = pd.DataFrame(index=range(len(df_weather) - 1)).reindex(df_weather.index)
        df_rule['TMPrule1'], df_rule['TMPrule2'] = 3, 30
        df_rule['WSDrule'], df_rule['PCPrule'], df_rule['SNOrule'] = 10, 3, 2

        # 다단계 기준 적용, 더 촘촘한 기준으로 변경
        df_weather['isoutside'] = True  # 기본적으로 실외
        conditions = [
                (df_weather['TMP'] < df_rule['TMPrule1']),
                (df_weather['TMP'] > df_rule['TMPrule2']),
                (df_weather['WSD'] > df_rule['WSDrule']),
                (df_weather['PCP'] > df_rule['PCPrule']),
                (df_weather['SNO'] > df_rule['SNOrule']),
                (df_weather['TMP'] >= 25),
                (df_weather['PCP'] >= 0.5),
            ]
        for cond in conditions:
            df_weather.loc[cond, 'isoutside'] = False

        df_weather_outside = df_weather[['datefcst', 'isoutside', 'TMP', 'PCP']].copy()
        df_weather_outside['datefcst'] = pd.to_datetime(df_weather_outside['datefcst'])

        # MySQL에서 스케줄 가져오기
        df_schedule = pd.DataFrame(get_kindergarten_schedule())
        df_schedule['datefcst'] = pd.to_datetime(df_schedule['datetime']).dt.round('h')
        df_schedule['original_isoutside'] = df_schedule['isoutside']  # 원래 상태 저장

        # 변경된 스케줄 탐지
        changed_schedules = pd.merge(df_weather_outside, df_schedule, on='datefcst', how='inner')
        changed_schedules = changed_schedules[changed_schedules['isoutside_x'] != changed_schedules['isoutside_y']]
        changed_schedules['weather_reason'] = changed_schedules.apply(
            lambda row: f"온도 {row['TMP']}°C, 강수량 {row['PCP']}mm로 인해 {'실내' if not row['isoutside_x'] else '실외'}로 변경", 
        axis=1
    )
        

        result = changed_schedules.rename(columns={
        'isoutside_x': 'isoutside',  # 변경 후 상태
        'isoutside_y': 'originalIsOutside'  # 원래 상태
        })[['datefcst', 'minutes', 'program', 'isoutside', 'originalIsOutside', 'teacher', 'weather_reason']]
        print(f"변경된 스케줄 수: {len(result)}")
        return result.to_dict(orient='records') if not result.empty else []

def generate_gemini_message(changed_schedules):
    if not changed_schedules:
        return "변경된 일정이 없습니다."
    prompt = f"""
    너는 유치원 선생님이야. 학부모님께 안내 문자를 보내야 하는 상황이야. 어투는 ~해요 체를 쓰고, 친근하게 써줘.
    다음은 날씨로 인해 변경된 유치원 스케줄입니다:
    {pd.DataFrame(changed_schedules).to_string()}
    학부모님께 보내는 친근한 안내 메시지를 작성해줘.
    """
    print(f"Gemini에 보내는 프롬프트: {prompt}")
    try:
        print("Gemini API 호출 시작")
        response = model.generate_content(prompt)  # system_instruction 제거
        print(f"Gemini 응답: {response.text}")
        return response.text
    except Exception as e:
        print(f"Gemini API 오류: {str(e)}")
        return f"변경된 일정 안내:\n{pd.DataFrame(changed_schedules).to_string()}"

def get_changed_schedules(nx: int = 62, ny: int = 126):
    print("get_changed_schedules 시작")
    advisor = WeatherActivityAdvisor(WEATHER_API_SERVICE_KEY)
    print("날씨 예보 가져오기 시작")
    advisor.get_weather_forecast_by_date(nx, ny)
    print("날씨 데이터 처리 시작")
    advisor.process_weather_data()
    print("의사결정 시작")
    try:
        changed_schedules = advisor.decision_making()
    except Exception as e:
        print(f"의사결정 오류: {str(e)}")
        changed_schedules = []
    print(f"변경된 스케줄: {changed_schedules}")
    print("Gemini 메시지 생성 시작")
    message = generate_gemini_message(changed_schedules)
    print(f"생성된 메시지: {message}")
    return {"changed_schedules": changed_schedules, "message": message}

def get_kindergarten_schedule():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT start AS datetime, 
                   TIMESTAMPDIFF(MINUTE, start, end) AS minutes, 
                   program, 
                   isOutside AS isoutside, 
                   teacher 
            FROM schedule
        """
        cursor.execute(query)
        schedules = cursor.fetchall()
        print(f"MySQL 데이터 행 수: {len(schedules)}")
        return schedules
    except Exception as e:
        print(f"MySQL 조회 오류: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()