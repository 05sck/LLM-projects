import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_upstage import UpstageEmbeddings
from rag_process.config import UPSTAGE_API_KEY

# TXT 파일 로드
with open("medicine_texts_ver3.txt", "r", encoding="utf-8") as f:
    text_data = f.read().strip()

# 🔹 1. 연속된 줄바꿈을 통일된 구분자로 변경 (제품명 변경 시 사용)
text_data = re.sub(r"\n{3,}", "|||", text_data)  # 3개 이상의 개행 → "|||"

# 🔹 2. LangChain 청킹 설정 (구분자 설정)
text_splitter = RecursiveCharacterTextSplitter(
    separators=["|||", "\n\n", "\n"],  # 제품 변경: "|||", 문단: "\n\n", 문장: ". "
    chunk_size=800,  # 청크 크기
    chunk_overlap=100,  # 문맥 유지용 오버랩
)

# 🔹 3. 청크화 실행
chunks = text_splitter.split_text(text_data)

# 🔹 4. 결과 확인
for i, chunk in enumerate(chunks[10:20]):  # 처음 5개 청크만 확인
    print(f"청크 {i+1}:\n{chunk}\n{'-'*50}")



# API_KEY = os.getenv("GEMINI_API_KEY")

# embeddings_model = GoogleGenerativeAIEmbeddings(model='models/embedding-001', google_api_key=API_KEY) # 임베딩 모델 선택해야함

embeddings_model = UpstageEmbeddings(model = "embedding-query", api_key = UPSTAGE_API_KEY)

documents = [Document(page_content=text) for text in chunks]

vectorstore = FAISS.from_documents(documents=documents, embedding=embeddings_model)

# FAISS 로컬 저장
vectorstore.save_local("medicine_faiss_upstage_ver3")

print("FAISS 벡터 DB 저장 완료!")