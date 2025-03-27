import sys
from datetime import datetime, timedelta
from pathlib import Path

import mysql.connector
import pandas as pd
from mysql.connector import Error

# backend/를 모듈 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.config.mysql_config import config as db_config

# CSV 파일 경로
BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / 'app/services/kindergarten_schedule.csv'

try:
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

    # 데이터를 리스트로 준비 (execute 대신 executemany 사용 가능)
    data_to_insert = []
    for index, row in df.iterrows():
        try:
            start_time = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')
            end_time = start_time + timedelta(minutes=int(row['minutes']))
            is_outside = 1 if row['isoutside'] in [True, 'True', 1] else 0  # 다양한 형식 처리
            data_to_insert.append((
                start_time,
                end_time,
                row['program'],
                None,
                row['teacher'],
                0.0,
                0.0,
                is_outside
            ))
        except ValueError as e:
            print(f"행 {index}에서 데이터 변환 오류: {e}")
            continue

    # 여러 행을 한 번에 삽입
    cursor.executemany(insert_query, data_to_insert)

    # 커밋
    conn.commit()
    print(f"{cursor.rowcount}개의 데이터가 MySQL에 성공적으로 삽입되었습니다.")

except FileNotFoundError:
    print(f"CSV 파일을 찾을 수 없습니다: {csv_path}")
except Error as e:
    print(f"MySQL 연결 또는 쿼리 실행 중 오류: {e}")
    if conn.is_connected():
        conn.rollback()
except Exception as e:
    print(f"예상치 못한 오류 발생: {e}")
finally:
    # 연결 종료
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("MySQL 연결이 종료되었습니다.")