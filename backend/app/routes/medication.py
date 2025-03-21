from app.services import db_service, line_send_message
from fastapi import APIRouter

router = APIRouter()

@router.get("/api/medications")
def get_medications():
    return {"medications": db_service.get_medications()}

@router.get("/api/children")
def get_children():
    return {"children": db_service.get_children()}

@router.post("/api/medications/confirm")
def confirm_medication(child_id: int, med: str):
    return {"message": db_service.confirm_medication(child_id, med)}

@router.get("/api/medication_logs")
def get_medication_logs():
    return {"logs": db_service.get_medication_logs()}

@router.post("/api/medications/log")
def add_medication_log(child_id: int, med_id: int, dosage: str, given_by: str):
    result = db_service.add_medication_log(child_id, med_id, dosage, given_by)
    if result:
        message = f"{result['child_name']}에게 {dosage}의 {result['med_name']}가 {given_by}에 의해 투약되었습니다."
        if result['line_id']:
            success = line_send_message.send_line_message(result['line_id'], message)
            return {"message": "투약 기록 추가 및 LINE 전송 완료" if success else "LINE 전송 실패"}
    return {"message": "투약 기록 추가 실패"}