#Stremalit 앱으로 진입. UI 레이아웃과 흐름을 정의.
# 절대 경로

import os
import sys

sys.path.append("C:/test")
import streamlit as st

from services.db_service import db_name, db_phone
from services.line_send_message import send_line_message
from services.llm_service import llm_fuc

names=db_name()
phones=db_phone()

CHANNEL_ACCESS_TOKEN="U5mOtIoUbFJ5K9L1cZJ3bqiMEEbA/aRriHqEU4IEntdiu4D7Ncr+C5YwxWSzAYAnXVYTNCDSbaC+rQdrxO/Lsjv7/bXOaqyFBqxxRVJp2IDwFMd1VgIhFfU0UMXK2YlPBISylCrSCK5K+h1xDCXdKgdB04t89/1O/w1cDnyilFU="
USER_ID="Uaecc6981aace6cd3c6788ffb6019f1ff" #Reciever

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


