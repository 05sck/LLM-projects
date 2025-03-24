# !pip install -q -U google-genai
# !pip install python-dotenv 
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

sys.path.append("C:/test")
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
print("API 키가 정상적으로 로드되었습니다!")

client = genai.Client(api_key=API_KEY)

def llm_fuc(event: str, date: str, reason: str) -> str:
    print(f"llm_fuc 호출 - event: {event}, date: {date}, reason: {reason}")
    prompt = f"'{event}' 일정이 {date}로 변경되었어요. 변경 사유는 '{reason}'이에요. 학부모님께 보내는 친근한 안내 메시지를 작성해줘."
    sys_instruct = """너는 유치원 선생님이야. 학부모님께 안내 문자를 보내야 하는 상황이야. 어투는 ~해요 체를 쓰고, 친근하게 써줘.
    예시는 다음과 같아.
    안녕하세요, 학부모님!
    우리 아이들과 함께할 '소풍' 일정이 2025-03-25로 변경되었어요!
    변경 사유는 '비가 올 것 같아서'예요.
    날씨에 맞춰서 아이들이 더 즐겁게 놀 수 있도록 준비해주세요!
    좋은 하루 되세요!
    """
    try:
        print("Gemini API 호출 시작")  # 디버깅
        response = client.models.generate_content(
            model="gemini-1.5-pro",
            config=types.GenerateContentConfig(system_instruction=sys_instruct),
            contents=prompt
        )
        print("Gemini API 응답 수신")  # 디버깅
        text = response.text
        # typecheck = type(response.text)
        return text
    except Exception as e:
        print(f"Gemini API 오류: {str(e)}")  # 디버깅
        return f"오류: {str(e)}"