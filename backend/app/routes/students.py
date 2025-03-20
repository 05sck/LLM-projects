from fastapi import APIRouter

router = APIRouter()

@router.get("/api/students/count")
def get_student_count():
    return {"count": 30}