import logging

from app.services import db_service  # 엔드포인트 정의
from fastapi import APIRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def read_root():
    logger.info("Root endpoint called")
    total_students = db_service.get_student_count()
    logger.info(f"Student count: {total_students}")
    return {"message": "Hello, World!", "total_students": total_students}