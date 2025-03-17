import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from rag_process.config import GEMINI_API_KEY, FAISS_DB_PATH

# 환경 변수 로드
load_dotenv()

def load_vector_db():
    """FAISS 벡터 DB 로드 함수"""
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)
    vectorstore = FAISS.load_local(FAISS_DB_PATH, embeddings_model, allow_dangerous_deserialization=True)
    
    print("FAISS 벡터 DB 로드 완료!")
    return vectorstore
