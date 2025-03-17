import json

# JSON 데이터 로드
with open("filtered_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 변환된 텍스트 저장 리스트
formatted_texts = []

# JSON → 텍스트 변환 함수
def json_to_text(item):
    return f"""제품명: {item.get('itemName', '제품명 없음')}
제조사: {item.get('entpName', '제조사 없음')}
[효능]
{item.get('efcyQesitm', '효능 정보 없음')}
[사용법]
{item.get('useMethodQesitm', '사용법 정보 없음')}
[주의사항 경고]
{item.get('atpnWarnQesitm', '주의사항 경고 없음')}
[주의사항]
{item.get('atpnQesitm', '주의사항 없음')}
[상호작용]
{item.get('intrcQesitm', '상호작용 정보 없음')}
[부작용]
{item.get('seQesitm', '부작용 정보 없음')}
[보관법]
{item.get('depositMethodQesitm', '보관법 없음')}
"""

# 변환 실행
for item in data:
    formatted_texts.append(json_to_text(item))

# txt 파일로 저장
with open("medicine_texts.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(formatted_texts))

print("JSON 데이터가 txt로 변환 및 저장되었습니다!")
