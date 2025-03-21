import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_upstage import UpstageEmbeddings
from config import UPSTAGE_FAISS_DB_PATH, UPSTAGE_API_KEY
from config import OPEN_API_KEY, OPENAI_MODEL_NAME, MAX_OUTPUT_TOKENS, TEMPERATURE, TOP_P

#임베딩 모델 및 저장된 벡터 DB 로드
embeddings_model = UpstageEmbeddings(model="embedding-query", api_key=UPSTAGE_API_KEY)
vectorstore = FAISS.load_local(UPSTAGE_FAISS_DB_PATH, embeddings_model, allow_dangerous_deserialization=True)

#Generator 모델
openai_model = ChatOpenAI(
    model=OPENAI_MODEL_NAME,
    openai_api_key=OPEN_API_KEY,
    max_tokens=MAX_OUTPUT_TOKENS,
    temperature=TEMPERATURE,
    top_p=TOP_P
)

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY

#프롬프트 구성

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import SystemMessage

# 파일에서 프롬프트 내용을 읽어오는 함수
def load_prompt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        prompt = file.read().strip()
    return prompt

# 🟢 1. System 프롬프트 (역할 정의)
prompt_template = load_prompt("rag_process/system_prompt.txt")


system_prompt_template = prompt_template.format(
    name="홍성준", age="6세", gender="남자", weight="15kg", height="120cm",
    status="어머님이 요청하신대로 등원 직후 부루펜 100mg 복용하려 하였으나 점심을 먹지 복용하지 못한 상황황"
)

formatted_system_prompt = SystemMessage(content=system_prompt_template)


# 🟢 2. User 프롬프트 (질문 & context)
template = load_prompt("rag_process/prompt.txt")

prompt = ChatPromptTemplate.from_messages([formatted_system_prompt, template])

# Retriever 설정정
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2}
)

chain = (
        {"context": retriever, "query": RunnablePassthrough()}
        | prompt
        | openai_model
        | StrOutputParser()
    )

question = input("질문을 입력하세요: ")

retrieved_docs = retriever.invoke(question)  
print("검색된 문서:")
for i, doc in enumerate(retrieved_docs):
    print(f"\n🔹 문서 {i+1}:\n{doc.page_content}")

response = chain.invoke(question)

print(response)