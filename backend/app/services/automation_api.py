# backend/app/services/automation_api.py
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

import google.generativeai as genai  # Gemini 추가
import numpy as np
import pandas as pd
import requests
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

        df_weather['isoutside'] = np.where(
            (df_weather['TMP'] < df_rule['TMPrule1']) | (df_weather['TMP'] > df_rule['TMPrule2']) |
            (df_weather['WSD'] > df_rule['WSDrule']) | (df_weather['PCP'] > df_rule['PCPrule']) |
            (df_weather['SNO'] > df_rule['SNOrule']), True, False)

        df_weather_outside = df_weather[['datefcst', 'isoutside']].copy()  # .copy() 추가
        df_weather_outside.loc[:, 'datefcst'] = pd.to_datetime(df_weather_outside['datefcst'])  # .loc 사용

        df_schedule = pd.read_csv(BASE_DIR / 'kindergarten_schedule.csv')
        df_schedule.rename(columns={'datetime': 'datefcst'}, inplace=True)
        df_schedule_outside = df_schedule[df_schedule['isoutside'] == True].copy()  # .copy() 추가
        df_schedule_outside.loc[:, 'datefcst'] = pd.to_datetime(df_schedule_outside['datefcst']).dt.round('h')  # 'H'를 'h'로 변경, .loc 사용
        print(f"Loaded CSV: {df_schedule.to_string()}")
        print(f"df_weather_outside: {df_weather_outside.head().to_string()}")
        print(f"df_schedule_outside: {df_schedule_outside.head().to_string()}")
        changed_schedules = pd.merge(df_weather_outside, df_schedule_outside, on=['datefcst', 'isoutside'], how='inner')
        print(f"merged result: {changed_schedules.head().to_string()}")
        print(f"변경된 스케줄 수: {len(changed_schedules)}")
        return changed_schedules.to_dict(orient='records') if not changed_schedules.empty else []

def generate_gemini_message(changed_schedules):
    if not changed_schedules:
        return "변경된 일정이 없습니다."
    prompt = f"""
    다음은 날씨로 인해 변경된 유치원 스케줄입니다:
    {pd.DataFrame(changed_schedules).to_string()}
    학부모님께 보내는 친근한 안내 메시지를 작성해줘.
    """
    sys_instruct = """너는 유치원 선생님이야. 학부모님께 안내 문자를 보내야 하는 상황이야. 어투는 ~해요 체를 쓰고, 친근하게 써줘."""
    print(f"Gemini에 보내는 프롬프트: {prompt}")
    try:
        print("Gemini API 호출 시작")
        response = model.generate_content(
            contents=prompt,
            generation_config={"system_instruction": sys_instruct}
        )
        print(f"Gemini 응답: {response.text}")
        return response.text
    except Exception as e:
        print(f"Gemini API 오류: {str(e)}")
        return f"오류: {str(e)}"

def get_changed_schedules(nx: int = 62, ny: int = 126):
    print("get_changed_schedules 시작")
    advisor = WeatherActivityAdvisor(WEATHER_API_SERVICE_KEY)
    print("날씨 예보 가져오기 시작")
    advisor.get_weather_forecast_by_date(nx, ny)
    print("날씨 데이터 처리 시작")
    advisor.process_weather_data()
    print("의사결정 시작")
    changed_schedules = advisor.decision_making()
    print(f"변경된 스케줄: {changed_schedules}")
    print("Gemini 메시지 생성 시작")
    message = generate_gemini_message(changed_schedules)
    print(f"생성된 메시지: {message}")
    return {"changed_schedules": changed_schedules, "message": message}

def get_kindergarten_schedule():
    file_path = BASE_DIR / 'kindergarten_schedule.csv'
    print(f"CSV 파일 경로: {file_path}")
    if not file_path.exists():
        print(f"파일이 존재하지 않습니다: {file_path}")
        return []
    df_schedule = pd.read_csv(file_path)
    print(f"CSV 데이터 행 수: {len(df_schedule)}")
    return df_schedule.to_dict(orient='records')