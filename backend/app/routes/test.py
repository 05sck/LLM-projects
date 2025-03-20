from fastapi import APIRouter  # 테스트 엔드포인트 정의

router = APIRouter()

@router.get("/test")
async def test_endpoint():
    return {"status": "success", "data": "This is a test endpoint"}