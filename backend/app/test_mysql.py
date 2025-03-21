import mysql.connector
from mysql.connector import Error

# GCP MySQL 접속 정보
config = {
    "host": "34.64.108.208",      # GCP MySQL 공용 IP
    "user": "root",              # 사용자 이름
    "password": "0000",  # 비밀번호
    "database": "kindergarten_notify" # 데이터베이스 이름
}

try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("MySQL 연결 성공!")
        print(f"서버 버전: {connection.get_server_info()}")
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()[0]
        print(f"현재 데이터베이스: {db_name}")
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print(f"테이블 목록: {tables}")
        cursor.close()
        connection.close()
except Error as e:
    print(f"MySQL 연결 실패: {e}")