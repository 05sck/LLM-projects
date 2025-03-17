from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from rag_process.retriever import retrieve_documents
from rag_process.config import GEMINI_API_KEY, GEMINI_MODEL_NAME, MAX_OUTPUT_TOKENS, TEMPERATURE, TOP_P, TOP_K

def create_rag_chain():
    """RAG 체인 생성"""
    # Gemini 1.5 Pro 모델 설정
    gemini_model = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL_NAME,
        google_api_key=GEMINI_API_KEY,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        top_k=TOP_K
    )

    # 프롬프트 설정
    prompt = PromptTemplate.from_template(
        """당신은 의료 정보를 제공하는 AI입니다.
        다음 문서 내용을 참고하여 질문에 답하세요.
        만약 문서에서 답을 찾을 수 없다면, 모른다고 말하세요.

        # 문서 내용:
        {context}

        # 질문:
        {question}

        # 답변:"""
    )

    # RAG 체인 실행 가능하도록 수정
    retriever = retrieve_documents  # 검색 함수 연결

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}  # 검색 결과와 질문 전달
        | prompt
        | gemini_model
        | StrOutputParser()
    )

    return rag_chain  # 실행 가능한 체인 객체 반환
