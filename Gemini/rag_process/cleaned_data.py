import json

# JSON 파일 경로
input_file = "rag_process/filtered_data.json"
output_file = "rag_process/filtered_data_cleaned.json"

# JSON 데이터 로드
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# 모든 텍스트 필드에서 \n 제거
def clean_newlines(obj):
    if isinstance(obj, dict):
        return {key: clean_newlines(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [clean_newlines(item) for item in obj]
    elif isinstance(obj, str):
        return obj.replace("\n", " ")  # \n을 공백으로 변환
    return obj

cleaned_data = clean_newlines(data)

# 새로운 JSON 파일로 저장
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

print("줄바꿈 문자가 제거된 JSON 파일이 저장되었습니다:", output_file)
