import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from openai import OpenAI

# 🔒 Firestore 인증

if firebase_admin._apps:
    firebase_admin.delete_app(firebase_admin.get_app())
    
cred = credentials.Certificate(r"C:\Users\Hoon\nipa\firebase\config\test-2b839-firebase-adminsdk-fbsvc-a9a8ef493c.json.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 🔒 OpenAI API 키
api_key = "sk-IWn5Q3VNPxc96nWRLjUC_bZrkLREbaPyYlUjcg8bNdT3BlbkFJ730aN105iwHWVMVDMA1f82EzJO-3viXnn1VZjNvy4A"
client = OpenAI(api_key=api_key)

# 📢 Streamlit UI
st.title("📢 유치원 문자 알림 서비스")

# ✅ Firestore에서 학부모 데이터 가져오기
collection_ref = db.collection("users")
docs = collection_ref.stream()
parents_list = [doc.id for doc in docs]  # 학부모 이름 리스트 생성

# 📌 학부모 선택 (Firestore 데이터 기반)
selected_parent = st.selectbox("👨‍👩‍👦 학부모 선택", parents_list)

# 🔹 선택한 학부모의 연락처 가져오기
if selected_parent:
    parent_data = db.collection("users").document(selected_parent).get().to_dict()
    parent_number = parent_data.get("phone", "전화번호 없음")  # 예: "010-1234-5678"
    st.text(f"📞 {selected_parent} 님의 연락처: {parent_number}")

# 📌 공지 유형 선택
message_type = st.selectbox("📌 메시지 유형 선택", ["일반 알림", "긴급 공지", "가정 통신문"])

# 🔹 상황 입력
situation = st.text_area("📝 어떤 상황인가요?", "예: 내일 소풍 일정 변경 안내")

# ✅ GPT-4로 개인화된 메시지 자동 생성
if st.button("✨ 메시지 자동 생성"):
    if not situation.strip():
        st.warning("⚠️ 상황을 입력해주세요!")
    else:
        prompt = f"""
        {selected_parent} 학부모님께 보낼 유치원 공지 메시지를 작성해줘:
        - 유형: {message_type}
        - 상황: {situation}
        - 톤: 친근하고 간결하게
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}]
            )
            generated_message = response.choices[0].message.content
            st.text_area("💬 생성된 메시지", generated_message, height=150)
        
        except Exception as e:
            st.error(f"❌ 메시지 생성 중 오류 발생: {e}")

# 🔹 최종 메시지 수정 가능
custom_message = st.text_area("✍️ 최종 메시지", generated_message if "generated_message" in locals() else "")

# 📤 메시지 전송
if st.button("📤 메시지 전송"):
    if custom_message.strip():
        st.success(f"✅ {selected_parent} 학부모님께 성공적으로 전송되었습니다!\n\n📩 보낸 메시지:\n{custom_message}")
    else:
        st.warning("⚠️ 메시지를 입력하세요.")
