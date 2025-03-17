from rag_process.gemini_rag import create_rag_chain

def main():
    """RAG 실행"""
    # RAG 체인 생성
    rag_chain = create_rag_chain()  # 올바른 체인 객체 반환

    query = input("\n질문을 입력하세요: ")

    # 체인 실행
    response = rag_chain.invoke(query)

    print("\nGemini RAG 답변:")
    print(response)

if __name__ == "__main__":
    main()
