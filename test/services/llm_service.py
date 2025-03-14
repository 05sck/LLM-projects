# !pip install -q -U google-genai
# !pip install python-dotenv 

# 절대 경로

import os
import sys

sys.path.append("C:/test")

#API KEY

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")

print("API 키가 정상적으로 로드되었습니다!")  # 테스트용 출력

from google import genai
from google.genai import types

client = genai.Client(api_key=API_KEY)

def llm_fuc(name,phone) :

    prompt = f"내일 숲 체험 학습이 예정되어 있는데, 날씨가 쌀쌀하니 {name}에게 따뜻한 옷과 장갑을 꼭 챙겨 보내달라는 내용을 작성해줘 번호:{phone}를 마지막에 작성해줘."
    sys_instruct = """너는 유치원 선생님이야. 학부모님께 안내 문자를 보내야 하는 상황이야. 어투는 ~해요 체를 쓰고, 친근하게 써줘.
    예시는 다음과 같아.
    안녕하세요, 성준 어머님!
    내일 우리 친구들과 함께 신나는 숲 체험 학습을 떠나는 날이에요!
    그런데 내일 날씨가 조금 쌀쌀할 것 같아요. 
    성준이가 감기 걸리지 않고 즐겁게 숲 체험을 할 수 있도록 따뜻한 옷과 장갑을 꼭 챙겨 보내주세요! 
    특히 바람막이 점퍼나 도톰한 외투가 있으면 더욱 좋을 것 같아요.
    좋은 하루 되세요! 
    """

    response = client.models.generate_content(
        model="gemini-1.5-pro",
        config = types.GenerateContentConfig(
            system_instruction = sys_instruct),
        contents=prompt
    )
    text=response.text
    #typecheck=type(response.text)

    return text