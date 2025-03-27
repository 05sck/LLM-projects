# backend/app/services/automation_api.py
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

import google.generativeai as genai
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
        self.base_date = now.strftime("%Y%m%d")
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
        print("process_weather_data 시작")
        try:
            df = self.weather_data
            df = df.pivot(index=['baseDate', "fcstDate", 'fcstTime', 'nx', 'ny', 'baseTime'], 
                          columns='category', values='fcstValue').reset_index()
            df.insert(0, 'datefcst', pd.to_datetime(df['fcstDate'].astype(str) + df['fcstTime'].str.zfill(4), format='%Y%m%d%H%M'))
            df.insert(0, 'datenow', pd.to_datetime(df['baseDate'].astype(str) + df['baseTime'].str.zfill(4), format='%Y%m%d%H%M'))
            df['PCP'] = df['PCP'].replace('강수없음', 0)
            df['SNO'] = df['SNO'].replace('적설없음', 0)
            df['PCP'] = df['PCP'].astype(str).apply(extract_float)
            df.drop(columns=['baseDate', 'baseTime', 'fcstDate', 'fcstTime', 'WAV', 'UUU', 'TMN', 'TMX', 'VEC', 'VVV'], inplace=True)
            self.weather_data = df
            df.to_csv(BASE_DIR / 'weather_data_refined.csv', index=False)
            print("process_weather_data 완료")
            return df
        except Exception as e:
            print(f"process_weather_data 오류: {str(e)}")
            raise

    def update_schedule_in_db(self, changed_schedules):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            updated_count = 0
            for schedule in changed_schedules:
                query = """
                UPDATE schedule 
                SET isOutside = %s, weather_reason = %s 
                WHERE start = %s AND program = %s
                """
                values = (
                    schedule['isoutside'],
                    schedule['weather_reason'],
                    schedule['datefcst'],
                    schedule['program']
                )
                print(f"DB 업데이트 시도: {schedule['datefcst']} - {schedule['program']} - isOutside: {schedule['isoutside']}")
                cursor.execute(query, values)
                if cursor.rowcount > 0:
                    updated_count += cursor.rowcount
                    print(f"DB 업데이트 성공: {schedule['datefcst']} - {schedule['program']} - isOutside: {schedule['isoutside']} - Reason: {schedule['weather_reason']}")
                else:
                    print(f"DB 업데이트 실패 (변경 없음): {schedule['datefcst']} - {schedule['program']}")
            conn.commit()
            print(f"DB에 총 {updated_count}개의 스케줄 업데이트 완료")
        except Exception as e:
            print(f"DB 업데이트 오류: {str(e)}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def decision_making(self):
        print("decision_making 메서드 실행 시작")
        try:
            df_weather = pd.read_csv(BASE_DIR / 'weather_data_refined.csv')
            print(f"날씨 데이터 행 수: {len(df_weather)}")
            print(f"날씨 데이터 샘플: \n{df_weather[['datefcst', 'TMP', 'WSD', 'PCP', 'SNO']].head().to_string()}")
        except Exception as e:
            print(f"날씨 데이터 로드 오류: {str(e)}")
            raise

        try:
            df_rule = pd.DataFrame(index=range(len(df_weather) - 1)).reindex(df_weather.index)
            df_rule['TMPrule1'], df_rule['TMPrule2'] = 3, 30
            df_rule['WSDrule'], df_rule['PCPrule'], df_rule['SNOrule'] = 10, 3, 2

            df_weather['isoutside'] = np.where(
                (df_weather['TMP'] < df_rule['TMPrule1']) |
                (df_weather['TMP'] > df_rule['TMPrule2']) |
                (df_weather['WSD'] > df_rule['WSDrule']) |
                (df_weather['PCP'] > df_rule['PCPrule']) |
                (df_weather['SNO'] > df_rule['SNOrule']),
                False, True
            )
            print(f"날씨 조건 적용 완료: 실외 가능 {df_weather['isoutside'].sum()}건, 실내 {len(df_weather) - df_weather['isoutside'].sum()}건")
        except Exception as e:
            print(f"날씨 조건 적용 오류: {str(e)}")
            raise

        df_weather_outside = df_weather[['datefcst', 'isoutside', 'TMP', 'PCP']].copy()
        df_weather_outside['datefcst'] = pd.to_datetime(df_weather_outside['datefcst'])

        try:
            df_schedule = pd.DataFrame(get_kindergarten_schedule())
            print(f"스케줄 데이터 행 수: {len(df_schedule)}")
            df_schedule['datefcst'] = pd.to_datetime(df_schedule['datetime']).dt.round('h')
            df_schedule['original_isoutside'] = df_schedule['isoutside']
        except Exception as e:
            print(f"스케줄 데이터 처리 오류: {str(e)}")
            raise

        changed_schedules = pd.merge(df_weather_outside, df_schedule, on='datefcst', how='inner')
        print(f"병합 후 데이터 행 수: {len(changed_schedules)}")
        changed_schedules = changed_schedules[changed_schedules['isoutside_x'] != changed_schedules['isoutside_y']]
        print(f"변경된 스케줄 탐지: {len(changed_schedules)}건")
        if not changed_schedules.empty:
            changed_schedules['weather_reason'] = changed_schedules.apply(
                lambda row: f"온도 {row['TMP']}°C, 강수량 {row['PCP']}mm로 인해 {'실내' if not row['isoutside_x'] else '실외'}로 변경",
                axis=1
            )
            print("변경된 스케줄 세부사항:")
            for index, row in changed_schedules.iterrows():
                print(f" - {row['datefcst']} - {row['program']}: {row['isoutside_y']} -> {row['isoutside_x']} ({row['weather_reason']})")

        result = changed_schedules.rename(columns={
            'isoutside_x': 'isoutside',
            'isoutside_y': 'originalIsOutside'
        })[['datefcst', 'minutes', 'program', 'isoutside', 'originalIsOutside', 'teacher', 'weather_reason']]

        if not result.empty:
            print("DB 업데이트 시작")
            self.update_schedule_in_db(result.to_dict(orient='records'))
            print("DB 업데이트 완료")
        else:
            print("변경된 스케줄 없음 - DB 업데이트 생략")

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
        response = model.generate_content(prompt)
        print(f"Gemini 응답: {response.text}")
        return response.text
    except Exception as e:
        print(f"Gemini API 오류: {str(e)}")
        return f"변경된 일정 안내:\n{pd.DataFrame(changed_schedules).to_string()}"

def test_function():
    print("테스트 함수 실행")
    return {"message": "테스트 성공"}

def get_changed_schedules(nx: int = 62, ny: int = 126):
    print("get_changed_schedules 시작")
    try:
        advisor = WeatherActivityAdvisor(WEATHER_API_SERVICE_KEY)
        print("WeatherActivityAdvisor 객체 생성 완료")
        print(f"advisor 속성 확인: {dir(advisor)}")
        print("날씨 예보 가져오기 시작")
        advisor.get_weather_forecast_by_date(nx, ny)
        print("날씨 데이터 처리 시작")
        advisor.process_weather_data()
        print("의사결정 시작")
        if hasattr(advisor, 'decision_making'):
            print("decision_making 메서드 존재 확인")
            changed_schedules = advisor.decision_making()
        else:
            print("decision_making 메서드 없음 - 클래스 정의 문제")
            raise AttributeError("'WeatherActivityAdvisor' object has no attribute 'decision_making'")
    except Exception as e:
        print(f"get_changed_schedules 오류: {str(e)}")
        import traceback
        print(traceback.format_exc())  # 스택 트레이스 출력
        changed_schedules = []
    print(f"변경된 스케줄: {changed_schedules}")
    print("Gemini 메시지 생성 시작")
    try:
        message = generate_gemini_message(changed_schedules)
    except Exception as e:
        print(f"Gemini 메시지 생성 오류: {str(e)}")
        message = "메시지 생성 중 오류 발생"
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