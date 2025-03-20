from app.routes import attendance, root, schedule, students, test
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5176"], # 테스트용, 나중에 "http://localhost:5173"과 같은 프론트엔드 URL로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(test.router)
app.include_router(students.router)
app.include_router(attendance.router)
app.include_router(schedule.router)