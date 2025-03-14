# db dataframe으로 가져오기
import os
import sys

sys.path.append("C:/test")
from config.firebase_config import db

#-----------------데이터베이스 읽기---------------------#


# 문서 선택 및 가져오기
#document_ref = db.document("test_name")
#doc = document_ref.get()

#데이터 읽기
#data=ref.get()
#print(data)


def db_name():
     collection_ref = db.collection("users")
     names = [doc.to_dict()["name"] for doc in collection_ref.stream()]
     return names


def db_phone():
     collection_ref = db.collection("users")
     phones = [doc.to_dict()["phone"] for doc in collection_ref.stream()]

     return phones