from app.routes import (attendance, medication, root, schedule, students, test,
                        weather)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # 테스트용, 나중에 "http://localhost:5173"과 같은 프론트엔드 URL로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(test.router)
app.include_router(students.router)
app.include_router(attendance.router)
app.include_router(schedule.router)
app.include_router(medication.router)
app.include_router(weather.router)  # weather 라우터 추가

'''
# Stremalit 앱으로 진입. UI 레이아웃과 흐름을 정의.
# 절대 경로

import os
import sys

sys.path.append("C:/test")
from datetime import datetime

import streamlit as st

from config.firebase_config import db
from services.db_service import db_name, db_phone
from services.line_send_message import send_line_message
from services.llm_service import llm_fuc

names=db_name()
phones=db_phone()

CHANNEL_ACCESS_TOKEN="U5mOtIoUbFJ5K9L1cZJ3bqiMEEbA/aRriHqEU4IEntdiu4D7Ncr+C5YwxWSzAYAnXVYTNCDSbaC+rQdrxO/Lsjv7/bXOaqyFBqxxRVJp2IDwFMd1VgIhFfU0UMXK2YlPBISylCrSCK5K+h1xDCXdKgdB04t89/1O/w1cDnyilFU="
USER_ID="Uaecc6981aace6cd3c6788ffb6019f1ff" #Reciever

# 📢 Streamlit UI
st.title("📢 유치원 문자 알림 서비스")


#------------일정 기능-------------#

st.markdown("## 일정변경")

title = st.text_input("제목")
new_date = st.date_input("일정 추가하기")
reason = st.text_input("변경 사유를 입력 해 주세요")



print(title)
print(new_date)

#정보 db 전달
if st.button("전송요청"):
    
    #파싱
    new_date=datetime.combine(new_date, datetime.min.time())
    date_str = new_date.strftime('%Y%m%d')  # "20250319"
    #document 이름 설정 -> document이름 비교로 갱신 여부 판단
    #동일 날짜 기준으로 단일 이벤트만 판단
    new_doc_id = date_str  # "20250319"
    
    # schedules 컬렉션에서 동일 날짜 문서 확인
    collection_name = 'schedules'
    doc_ref = db.collection(collection_name).document(new_doc_id)
    existing_doc = doc_ref.get()

    if existing_doc.exists:
            doc_data = existing_doc.to_dict()
            st.write("동일한 날짜의 기존 데이터 발견:")
            st.write(f"기존 문서 ID: {existing_doc.id}")
            st.write(f"기존 제목: {doc_data['title']}")
            st.write(f"기존 날짜: {date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}")

            # 기존 문서 갱신
            data = {
                'title': title,
                'new_date': new_date,
            }
            doc_ref.set(data)
            st.success(f"문서 ID {new_doc_id}가 새 데이터로 갱신되었습니다.")

    else:
            # 새 문서 추가
            data = {
                'title': title,
                'new_date': new_date,
            }
            doc_ref.set(data)
            st.success(f"새 문서가 추가되었습니다. 문서 ID: {new_doc_id}")

    print('데이터가 성공적으로 추가되었습니다.')

    #-----llm 으로 안내문 생성해서 전송하기 ----------#

#------------안내문 기능-------------#

st.markdown("## 안내문")
# 사용자의 질문 처리
st.header("질문하기")
question = st.text_input("질문을 입력하세요", "")

def main():

    results=[]
    if st.button("전송 요청"):
        # db 개수만큼 반복 출력 포문 두개
        for name, phone in zip(names,phones):
            if name=='youngho':
                result=llm_fuc(name,phone)
                results.append(result)
                st.write(f"이름:{name} 번호: {phone} 안내문: {result}")
                message=result
                send_line_message(CHANNEL_ACCESS_TOKEN, USER_ID, message)


#gemini test 버전 생성을 위해 주석
#    if st.button("전송 요청"):
#        # db 개수만큼 반복 출력 포문 두개
#        for name, phone in zip(names,phones):
#            result=llm_fuc(name,phone)
#            results.append(result)
#            st.write(f"이름:{name} 번호: {phone} 안내문: {result}")
#            if name=='youngho': 
#                send_line_message(channel_access_token,user_)    
        


if __name__=="__main__":
    main()


'''