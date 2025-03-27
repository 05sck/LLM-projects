# backend/app/routes/schedule.py
import os

from app.services import db_service, line_send_message
from app.services.automation_api import get_changed_schedules  # 새로 추가
from app.services.automation_api import get_kindergarten_schedule
from app.services.llm_service import llm_fuc
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/schedule", tags=["schedule"])  # prefix 추가로 URL 깔끔하게

@router.get("/api/schedule")
def get_schedule():
    return db_service.get_schedules()

@router.post("/api/schedule")
def add_schedule(date: str, event: str):
    return db_service.add_schedule(date, event)

@router.post("/api/send_line")
async def send_line(request: dict):
    message = request.get("message")
    user_id = request.get("user_id", "Uaecc6981aace6cd3c6788ffb6019f1ff")  # 기본값
    if not message:
        return {"message": "메시지를 입력해주세요", "status": 400}
    
    from ..services.line_send_message import CHANNEL_ACCESS_TOKEN
    success = line_send_message.send_line_message(CHANNEL_ACCESS_TOKEN, user_id, message)
    if success:
        return {"message": "LINE 메시지 전송 성공", "status": 200}
    return {"message": "LINE 전송 실패", "status": 500}

class MessageRequest(BaseModel):
    event: str
    date: str
    reason: str

@router.post("/api/send-message")
async def send_message(request: MessageRequest):
    print("엔드포인트 호출됨:", request.dict())
    result = llm_fuc(request.event, request.date, request.reason)
    print("결과 반환:", result)
    return {"status": "success", "message": result}

# 새로 추가된 엔드포인트
@router.get("/api/changed-schedules")
async def fetch_changed_schedules(nx: int = 62, ny: int = 126):
    print("changed-schedules 엔드포인트 호출됨")
    print(f"엔드포인트 호출됨: nx={nx}, ny={ny}")
    result = get_changed_schedules(nx=nx, ny=ny)  # automation_api에서 결과 가져오기
    return {
        "changed_schedules": result.get("changed_schedules", []),
        "message": result.get("message", "날씨 기반 일정 변경 메시지가 생성되었습니다.")
    }

@router.get("/api/schedules")
async def read_schedules():
    return get_kindergarten_schedule()