import json

# JSON 데이터 로드
input_file = "rag_process/filtered_data_cleaned.json"
output_file = "rag_process/medicine_texts_ver4.txt"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# 변환된 텍스트 저장 리스트
formatted_texts = []
previous_medicine_name = None  # 이전 제품명 추적

# JSON → 텍스트 변환 함수 (대괄호 유지, 카테고리별 청크 생성)
def json_to_text(item):
    categories = {
        "[효능]": item.get("efcyQesitm", "효능 정보 없음"),
        "[사용법]": item.get("useMethodQesitm", "사용법 정보 없음"),
        "[주의사항 경고]": item.get("atpnWarnQesitm", "주의사항 경고 없음"),
        "[주의사항]": item.get("atpnQesitm", "주의사항 없음"),
        "[상호작용]": item.get("intrcQesitm", "상호작용 정보 없음"),
        "[부작용]": item.get("seQesitm", "부작용 정보 없음"),
        "[보관법]": item.get("depositMethodQesitm", "보관법 없음"),
    }

    # 약 이름 추가
    medicine_name = item.get("itemName", "제품명 없음")

    # 카테고리별 청크 생성
    chunks = []
    for category, content in categories.items():
        if content and content.strip():  # 내용이 있는 경우만 추가
            chunk_title = f"{medicine_name} - {category}"
            chunk_text = f"{chunk_title}\n{content.strip()}"
            chunks.append(chunk_text)

    return medicine_name, chunks  # 제품명과 청크 반환

# 변환 실행
for item in data:
    medicine_name, chunks = json_to_text(item)

    # 제품명이 바뀌었을 때 '\n\n\n' 추가
    if previous_medicine_name and previous_medicine_name != medicine_name:
        formatted_texts.append("\n")  # 제품이 바뀌면 한 줄 더 띄움

    formatted_texts.extend(chunks)  # 여러 청크 추가
    previous_medicine_name = medicine_name  # 현재 제품명을 이전 제품명으로 업데이트

# txt 파일로 저장 (카테고리별로 나눈 텍스트를 한 줄씩 저장)
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n\n".join(formatted_texts))  

print("JSON 데이터가 제품명 변경 시 줄바꿈 추가되어 변환 및 저장되었습니다!")
