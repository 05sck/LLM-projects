import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# gemini API 키 설정
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # .env 파일에서 가져오기

# FAISS 저장 경로
FAISS_DB_PATH = "rag_process/medicine_faiss"

# Gemini 모델 기본 설정
GEMINI_MODEL_NAME = "gemini-1.5-pro"
MAX_OUTPUT_TOKENS = 500
TEMPERATURE = 0.3
TOP_P = 0.9
TOP_K = 40
