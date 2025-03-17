import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
decoding_key = os.getenv("service_key")

# 공공데이터 API URL
url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'

# 디코딩된 서비스 키 사용
service_key = decoding_key  # 공공데이터 API 키 입력

# 검색할 성분 목록
search_keywords = ["아세트아미노펜", "이부프로펜", "덱시부프로펜"]

# 최종 저장할 리스트
all_filtered_items = []

for keyword in search_keywords:
    params = {
        'serviceKey': service_key,
        'pageNo': '1',
        'numOfRows': '100',
        'type': 'json',
        'itemName': keyword  #특정 성분 검색
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            items = data.get("body", {}).get("items", [])

            # 검색된 약품 추가
            all_filtered_items.extend(items)

            print(f"'{keyword}' 포함된 제품 {len(items)}개 수집 완료!")

        except json.JSONDecodeError:
            print(f"JSON 변환 실패 (검색어: {keyword}). 원본 응답 출력:")
            print(response.text)
    else:
        print(f"API 요청 실패 (검색어: {keyword}): {response.status_code}")

# 필터링된 모든 데이터를 JSON으로 저장
with open("filtered_data.json", "w", encoding="utf-8") as f:
    json.dump(all_filtered_items, f, ensure_ascii=False, indent=2)

print(f"총 {len(all_filtered_items)}개의 필터링된 제품 저장 완료")