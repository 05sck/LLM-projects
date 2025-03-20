from fastapi import APIRouter  # 엔드포인트 정의의

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello, World!"}