#Stremalit 앱으로 진입. UI 레이아웃과 흐름을 정의.
# 절대 경로

import os
import sys

sys.path.append("C:/test")
import streamlit as st

from services.db_service import db_name, db_phone
from services.llm_service import llm_fuc

names=db_name()
phones=db_phone()

def main():

    results=[]

    if st.button("전송 요청"):
        # db 개수만큼 반복 출력 포문 두개
        for name, phone in zip(names,phones):
            result=llm_fuc(name,phone)
            results.append(result)
            st.write(f"이름:{name} 번호: {phone} 안내문: {result}")

if __name__=="__main__":
    main()


