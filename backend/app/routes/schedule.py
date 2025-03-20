from fastapi import APIRouter

router = APIRouter()

@router.get("/api/schedule/week")
def get_weekly_schedule():
    return [
        {"id": 1, "date": "2025-03-20", "name": "소풍"},
        {"id": 2, "date": "2025-03-22", "name": "체육대회"}
    ]