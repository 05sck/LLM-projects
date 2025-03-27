import sys
from datetime import datetime, timedelta
from pathlib import Path

import mysql.connector
import pandas as pd

# backend/를 모듈 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

# MySQL 연결 설정 가져오기
from app.config.mysql_config import config as db_config

# CSV 파일 경로
BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
csv_path = BASE_DIR / 'app/services/kindergarten_schedule.csv'

# CSV 읽기
df = pd.read_csv(csv_path)
print(f"CSV 데이터 행 수: {len(df)}")

# MySQL 연결
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 삽입 쿼리
insert_query = """
    INSERT INTO schedule (start, end, program, description, teacher, latitude, longitude, isOutside)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

# 데이터 삽입
for index, row in df.iterrows():
    start_time = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')
    end_time = start_time + timedelta(minutes=row['minutes'])
    cursor.execute(insert_query, (
        start_time,
        end_time,
        row['program'],
        None,                    # description
        row['teacher'],
        0.0,                     # latitude
        0.0,                     # longitude
        int(row['isoutside'])    # True/False -> 1/0
    ))

# 커밋 및 연결 종료
conn.commit()
print("데이터가 MySQL에 성공적으로 삽입되었습니다.")
cursor.close()
conn.close()