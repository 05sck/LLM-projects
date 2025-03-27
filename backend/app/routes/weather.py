import os

import pandas as pd
from app.services.automation_api import WeatherActivityAdvisor
from dotenv import load_dotenv
from fastapi import APIRouter

# 환경 변수 로드
load_dotenv()
WEATHER_API_SERVICE_KEY = os.getenv("WEATHER_API_SERVICE_KEY")

router = APIRouter(
    prefix="/weather",
    tags=["weather"]
)

@router.get("/")
async def get_current_weather(nx: int = 62, ny: int = 126):
    """
    현재 날씨 데이터를 반환합니다.
    - nx, ny: 기상청 격자 좌표 (기본값: 서울)
    - 반환: 기온(TMP)과 하늘 상태(SKY)
    """
    try:
        advisor = WeatherActivityAdvisor(WEATHER_API_SERVICE_KEY)
        advisor.get_weather_forecast_by_date(nx, ny)
        df = advisor.process_weather_data()
        
        # 현재 시간에 가장 가까운 날씨 데이터 선택
        now = pd.Timestamp.now()
        latest_weather = df.iloc[(df['datefcst'] - now).abs().argsort()[0]]
        
        return {
            "temperature": float(latest_weather["TMP"]),  # 기온
            "sky": latest_weather["SKY"]  # 하늘 상태 (1: 맑음, 3: 구름많음, 4: 흐림)
        }
    except Exception as e:
        return {"error": f"날씨 데이터를 가져오는 데 실패했습니다: {str(e)}"}