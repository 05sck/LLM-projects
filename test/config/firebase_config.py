import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 인증 정보를 제공하는 서비스 계정 키 파일을 다운로드하고 경로를 설정합니다.
cred = credentials.Certificate('C:/test/config/test-2b839-firebase-adminsdk-fbsvc-b99dbe5f3e.json')
#firebase 앱 초기화 
firebase_admin.initialize_app(cred) 

# Firebase 앱 초기화 실시간버전(realtime database)
#firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://test-2b839-default-rtdb.asia-southeast1.firebasedatabase.app/'
# })

# Firestore 데이터베이스를 가져옵니다.
db = firestore.client()
# realtime 방식
#ref=db.reference('/users') #컬렉션


'''
#----------------- 데이터베이스 삽입---------------------#
# 데이터를 추가할 컬렉션과 문서 ID를 설정합니다.
collection_name = 'users'
document_id = 'test_name' #지정하지 않을 경우 랜덤 id 생성

# 추가할 데이터를 딕셔너리 형태로 작성합니다.
data = {
    'name': 'John',
    'age': 30,
    'email': 'john@example.com'
}

# 데이터를 컬렉션에 추가합니다.
doc_ref = testdb.collection(collection_name).document(document_id)
doc_ref.set(data)

print('데이터가 성공적으로 추가되었습니다.')
'''