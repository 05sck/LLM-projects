import logging

from app.services import db_service, line_send_message
from app.services.LLM_projects.llm_service.rag_process import \
    process_medication_rag
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 기존 라우트 유지
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

# LINE 채널 액세스 토큰
CHANNEL_ACCESS_TOKEN = "U5mOtIoUbFJ5K9L1cZJ3bqiMEEbA/aRriHqEU4IEntdiu4D7Ncr+C5YwxWSzAYAnXVYTNCDSbaC+rQdrxO/Lsjv7/bXOaqyFBqxxRVJp2IDwFMd1VgIhFfU0UMXK2YlPBISylCrSCK5K+h1xDCXdKgdB04t89/1O/w1cDnyilFU="

# 새로운 라우터 (LINE 전송용)
class MedicationRequest(BaseModel):
    child_name: str
    med_name: str
    condition: str
    med_info: list
    line_id: str

@router.post("/api/send_line")
async def send_medication_line(request: MedicationRequest):
    enhanced_message = process_medication_rag(
        request.child_name,
        request.med_name,
        request.condition,
        request.med_info
    )
    line_send_message.send_line_message(CHANNEL_ACCESS_TOKEN, request.line_id, enhanced_message)
    return {"message": enhanced_message}

# 정보 조회 라우터 (웹 표시용)
@router.get("/medicine-info/")
async def get_medicine_info(
    request: Request,
    child_name: str,
    med_name: str,
    condition: str = "상황 없음",
    med_info: str = "기본 정보"
):
    logger.info(f"요청 URL: {request.url}")
    query_params = dict(request.query_params)
    logger.info(f"수신된 쿼리 파라미터: {query_params}")
    logger.info(f"파라미터 값: child_name='{child_name}', med_name='{med_name}', condition='{condition}', med_info='{med_info}'")
    try:
        med_info_list = [info.strip() for info in med_info.split(",") if info.strip()] if med_info else []
        logger.info(f"파싱된 med_info_list: {med_info_list}")
        result = process_medication_rag(child_name, med_name, condition, med_info_list)
        logger.info(f"RAG 결과: process_log={result['process_log']}, message={result['message']}")
        return {
            "process_log": result["process_log"],
            "message": result["message"]
        }
    except Exception as e:
        logger.error(f"RAG 처리 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"약 정보 조회 실패: {str(e)}")