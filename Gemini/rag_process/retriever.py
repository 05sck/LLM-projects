from rag_process.vector_db import load_vector_db

def retrieve_documents(query):
    """사용자의 질문을 기반으로 FAISS에서 문서 검색"""
    vectorstore = load_vector_db()
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})
    retrieved_docs = retriever.invoke(query)

    print("검색된 문서:")
    for i, doc in enumerate(retrieved_docs):
        print(f"\n🔹 문서 {i+1}:\n{doc.page_content}")

    return retrieved_docs
