from fastapi import APIRouter

router = APIRouter()

@router.get("/api/attendance/today")
def get_attendance_today():
    return {"present": 25, "late": 3, "absent": 2}