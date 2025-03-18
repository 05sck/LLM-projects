import streamlit as st
import sqlite3
import time
import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from openai import OpenAI

# 🔑 OpenAI API 설정
api_key = "YOUR_OPENAI_API_KEY"
client = OpenAI(api_key=api_key)

# 🔑 Google Calendar API 인증
calendar_cred = service_account.Credentials.from_service_account_file(
    r"C:\Users\Hoon\nipa\firebase\config\balmy-flash-415002-667db12f8bb3.json",
    scopes=["https://www.googleapis.com/auth/calendar"]
)
calendar_service = build("calendar", "v3", credentials=calendar_cred)
calendar_id = "primary"  # Google Calendar ID

# 🔹 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect("kindergarten.db")
    cursor = conn.cursor()
    
    # 학부모 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    # 일정 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            reason TEXT
        )
    ''')

    # 복약 테이블 생성 (몸무게 & 증상 추가)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medication_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT NOT NULL,
            weight REAL NOT NULL,  
            medicine TEXT NOT NULL,
            dosage TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            time TEXT NOT NULL,
            notes TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# 🔹 데이터베이스 초기화 실행
init_db()

# 🔹 학부모 정보 불러오기
def get_parents():
    conn = sqlite3.connect("kindergarten.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone FROM parents")
    parents = cursor.fetchall()
    conn.close()
    return parents


def update_db():
    conn = sqlite3.connect("kindergarten.db")
    cursor = conn.cursor()

    # 🔹 `children` 테이블이 없으면 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_contact TEXT NOT NULL,
            weight REAL DEFAULT 0
        )
    ''')

    # 🔹 weight 컬럼이 없는 경우 추가 (이미 존재하면 무시)
    try:
        cursor.execute("ALTER TABLE children ADD COLUMN weight REAL DEFAULT 0")
    except sqlite3.OperationalError:
        pass  # 이미 weight 컬럼이 있으면 무시

    # 🔹 기존 데이터 업데이트 (아이 이름이 없으면 추가)
    cursor.execute("INSERT OR IGNORE INTO children (name, parent_contact, weight) VALUES ('김민준', '010-1234-5678', 18.5)")
    cursor.execute("INSERT OR IGNORE INTO children (name, parent_contact, weight) VALUES ('박서연', '010-2345-6789', 16.0)")
    cursor.execute("INSERT OR IGNORE INTO children (name, parent_contact, weight) VALUES ('이지우', '010-3456-7890', 19.2)")

    conn.commit()
    conn.close()

# 실행
update_db()
# 🔹 아이 & 몸무게 정보 불러오기
def get_children():
    conn = sqlite3.connect("kindergarten.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, weight FROM children")
    children = cursor.fetchall()
    conn.close()
    return children

# 🔹 Google Calendar 일정 업데이트
def update_google_calendar(event_name, event_date, reason):
    try:
        # 기존 일정 검색
        events_result = calendar_service.events().list(calendarId=calendar_id, q=event_name, maxResults=1).execute()
        events = events_result.get("items", [])

        if events:
            event_id = events[0]["id"]
            event = calendar_service.events().get(calendarId=calendar_id, eventId=event_id).execute()
            event["start"]["date"] = event_date
            event["end"]["date"] = event_date
            event["description"] = reason
            calendar_service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
        else:
            event = {
                "summary": event_name + " 일정 변경",
                "start": {"date": event_date},
                "end": {"date": event_date},
                "description": reason
            }
            calendar_service.events().insert(calendarId=calendar_id, body=event).execute()

        return True
    except Exception as e:
        st.error(f"❌ Google Calendar 업데이트 실패: {e}")
        return False

# 📌 Streamlit UI
st.set_page_config(page_title="유치원 알림 시스템", layout="centered")
st.sidebar.title("🔍 메뉴 선택")

# 📌 사이드바 선택
menu = st.sidebar.radio("메뉴", ["📅 일정 변경 알림", "💊 복약 내용 알림"])

### **📅 일정 변경 알림**
if menu == "📅 일정 변경 알림":
    st.header("📅 일정 변경 알림")

    # 공지 유형 선택
    message_type = st.selectbox("📌 공지 유형 선택", ["일반 알림", "긴급 공지", "가정 통신문"])

    # 일정 정보 입력
    event_name = st.text_input("📅 일정명 입력", "소풍")
    event_date = st.date_input("📅 변경할 일정", datetime.date.today())
    reason = st.text_area("📝 변경 사유 입력", "우천 예보로 일정 변경")

    if st.button("📅 일정 변경 저장 및 알림 전송"):
        conn = sqlite3.connect("kindergarten.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO schedule (event_name, event_date, reason) VALUES (?, ?, ?)",
                       (event_name, event_date.strftime("%Y-%m-%d"), reason))
        conn.commit()
        conn.close()

        if update_google_calendar(event_name, event_date.strftime("%Y-%m-%d"), reason):
            st.success("✅ Google Calendar에 일정이 자동 업데이트되었습니다!")

        # 학부모 알림 전송 (시뮬레이션)
        for parent_name, parent_phone in get_parents():
            st.success(f"📩 {parent_name} ({parent_phone})에게 일정 변경 알림 전송 완료!")

### **💊 복약 내용 알림**
elif menu == "💊 복약 내용 알림":
    st.header("💊 복약 내용 알림")

    # 아이 선택
    children = get_children()
    if not children:
        st.warning("등록된 유치원생이 없습니다.")
        st.stop()
    child_name = st.selectbox("아이 선택", [c[0] for c in children])
    child_weight = next((c[1] for c in children if c[0] == child_name), None)

    # 아이 몸무게 표시
    st.write(f"🔹 아이 몸무게: {child_weight} kg")

    # 복약 정보 입력
    medicine = st.text_input("💊 약 이름")
    dosage = st.number_input("📏 용량 (ml)", min_value=0.0, step=0.5)
    symptoms = st.text_area("🤒 아이의 증상", placeholder="예: 발열, 기침, 콧물")
    time_input = st.time_input("⏰ 복용 시간")
    notes = st.text_area("📝 기타 사항")

    if st.button("💾 복약 기록 저장 및 알림 전송"):
        conn = sqlite3.connect("kindergarten.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medication_log (child_name, weight, medicine, dosage, symptoms, time, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (child_name, child_weight, medicine, f"{dosage}ml", symptoms, str(time_input), notes))
        conn.commit()
        conn.close()

        st.success("✅ 복약 기록이 저장되었습니다!")

        # 학부모 알림 전송 (시뮬레이션)
        parent_contact = next((p[1] for p in get_parents() if p[0] == child_name), "연락처 없음")
        st.success(f"📩 학부모({parent_contact})에게 알림 전송 완료!")

