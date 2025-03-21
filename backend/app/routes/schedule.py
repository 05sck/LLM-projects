from app.services import db_service, line_send_message
from fastapi import APIRouter

router = APIRouter()

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
    
    # line_send_message.py에서 하드코딩된 토큰 사용
    from app.services.line_send_message import CHANNEL_ACCESS_TOKEN
    success = line_send_message.send_line_message(CHANNEL_ACCESS_TOKEN, user_id, message)
    if success:
        return {"message": "LINE 메시지 전송 성공", "status": 200}
    return {"message": "LINE 전송 실패", "status": 500}

