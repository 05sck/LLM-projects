import firebase_admin
from firebase_admin import credentials, firestore

#DB json형태, number 유형 사용

# Firebase 인증 설정
cred = credentials.Certificate("C:/Users/hssj5/OneDrive/Desktop/seongjun/ml_bootcamp/test-2b839-firebase-adminsdk-fbsvc-b99dbe5f3e.json")
firebase_admin.initialize_app(cred) #firebase 앱 초기화


# Firestore 데이터베이스 클라이언트 생성
db = firestore.client()

#-----------------데이터베이스 조회---------------------#

# 'users' 콜렉션의 내용을 모두 가져오는 코드
collection_ref = db.collection("users")

# 콜렉션 안의 모든 문서 내용을 가져오는 코드
docs = collection_ref.stream()
for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")


'''
#----------------- 데이터베이스 삽입 코드(프로토타입에서 불필요)---------------------#
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
doc_ref = db.collection(collection_name).document(document_id)
doc_ref.set(data)

print('데이터가 성공적으로 추가되었습니다.')'
'''