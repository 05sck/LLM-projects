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

system_prompt = SystemMessage(content=
        """당신은 전문 상담원입니다. 아래 지침에 따라 사용자의 질문에 답변을 제공하세요.
        ---------------------
        1. 주어진 정보만 활용하여 답변을 제공하세요. 주어진 정보로 답변을 할 수 없는 경우, 정중하게 답변을 제공할 수 없다고 설명합니다.
        2. 답변은 정제된 형식과 문어체로 작성하며, 친절하고 자세한 내용을 제공합니다.
        ---------------------
        """
)

template = (
        "아래 context 정보를 참고하여 답변을 제공하세요.\n"
        "---------------------\n"
        "{context}"
        "\n---------------------\n"
        "주어진 context 정보를 보고, 가장 연관성 있는 {query} 청크를 제공하세요."
        "만약 주어진 정보에서 답을 찾을 수 없다면 '주어진 정보로 찾을 수 없습니다.'라고 출력하세요."
)

prompt = ChatPromptTemplate.from_messages([system_prompt, template])

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

from datasets import Dataset

import pandas as pd

# .xlsx 파일 경로 지정
file_path = 'rag_process/input.xlsx'

# .xlsx 파일을 읽어서 DataFrame으로 저장
data = pd.read_excel(file_path)

# 첫 번째 행의 'question'과 'ground_truths' 열 데이터를 리스트로 저장
questions = data['questions'].tolist()
ground_truths = data['ground_truths'].tolist()

# question과 ground_truths를 새로운 DataFrame으로 결합
result = pd.DataFrame({
    'questions': questions,
    'ground_truths': ground_truths
})

result

from tqdm import tqdm

answers = []
contexts = []

# Inference
for query in tqdm(questions):
  answers.append(chain.invoke(query))
  contexts.append([docs.page_content for docs in retriever.get_relevant_documents(query)])

# To dict
data = {
  "user_input": questions,
  "response": answers,
  "retrieved_contexts": contexts,
  "reference": ground_truths
}

# Convert dict to dataset
dataset = Dataset.from_dict(data)

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)

result = evaluate(
    dataset = dataset, 
    metrics=[
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy,
    ],
)

# score 출력
print(result)
# DataFrame 생성
df = result.to_pandas()
df.to_excel('rag_process/output.xlsx', index=False)
df