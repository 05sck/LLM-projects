import streamlit as st
from openai import OpenAI

# 🔒 API 키 불러오기
api_key = 

# OpenAI 클라이언트 생성
client = OpenAI(api_key=api_key)

# Streamlit UI
st.title("📢 유치원 문자 알림 서비스")

# 유치원 공지 유형 선택
message_type = st.selectbox("📌 메시지 유형 선택", ["일반 알림", "긴급 공지", "가정 통신문"])

# 🔹 추가: 사용자가 직접 상황을 입력
situation = st.text_area("📝 어떤 상황인가요?", "예: 내일 소풍 일정 변경 안내")

# GPT-4로 메시지 자동 생성
if st.button("✨ 메시지 자동 생성"):
    if not situation.strip():
        st.warning("⚠️ 상황을 입력해주세요!")
    else:
        prompt = f"""
        다음 상황에 맞춰 학부모에게 보낼 유치원 공지 메시지를 작성해줘:
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

# 학부모 대상 입력
parent_numbers = st.text_area("📞 보낼 학부모 연락처 (쉼표로 구분)", "010-1234-5678, 010-2345-6789")

# 🔹 미리보기 및 수정 가능하게 변경
custom_message = st.text_area("✍️ 최종 메시지", generated_message if "generated_message" in locals() else "")

# 메시지 전송 버튼
if st.button("📤 메시지 전송"):
    if custom_message.strip():
        st.success(f"✅ 메시지가 성공적으로 전송되었습니다!\n\n📩 보낸 메시지:\n{custom_message}")
    else:
        st.warning("⚠️ 메시지를 입력하세요.")
