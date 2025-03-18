import sqlite3
def update_db():
    conn = sqlite3.connect("kindergarten.db")
    cursor = conn.cursor()

    # 🔹 weight 컬럼 추가 (이미 존재하면 무시)
    try:
        cursor.execute("ALTER TABLE children ADD COLUMN weight REAL DEFAULT 0")
    except sqlite3.OperationalError:
        pass  # 이미 weight 컬럼이 있으면 무시

    # 🔹 기존 데이터 업데이트
    cursor.execute("UPDATE children SET weight = 18.5 WHERE name = '김민준'")
    cursor.execute("UPDATE children SET weight = 16.0 WHERE name = '박서연'")
    cursor.execute("UPDATE children SET weight = 19.2 WHERE name = '이지우'")

    conn.commit()
    conn.close()

# 실행
update_db()