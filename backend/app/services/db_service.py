from app.config.mysql_config import get_db


def get_student_count():
     db = get_db()
     if db:
          cursor = db.cursor()
          cursor.execute("SELECT COUNT(*) FROM children")
          count = cursor.fetchone()[0]
          cursor.close()
          db.close()
          return count
     return 0

def get_medications():
    db = get_db()
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT medication_id, name FROM medications")
        result = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        cursor.close()
        db.close()
        return result
    return []

def get_children():
    db = get_db()
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT child_id AS id, name, age, weight FROM children")
        result = [{"id": row[0], "name": row[1], "age": row[2], "weight": row[3]} for row in cursor.fetchall()]
        cursor.close()
        db.close()
        return result
    return []

def get_medication_logs():
    db = get_db()
    if db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT ml.log_id, c.name AS child_name, m.name AS med_name, ml.dosage, ml.time_given, ml.given_by
            FROM medication_logs ml
            JOIN children c ON ml.child_id = c.child_id
            JOIN medications m ON ml.medication_id = m.medication_id
        """)
        result = [
            {"log_id": row[0], "child_name": row[1], "med_name": row[2], "dosage": row[3], 
             "time_given": row[4].strftime("%Y-%m-%d %H:%M:%S"), "given_by": row[5]}
            for row in cursor.fetchall()
        ]
        cursor.close()
        db.close()
        return result
    return []

def add_medication_log(child_id, med_id, dosage, given_by):
    db = get_db()
    if db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO medication_logs (child_id, medication_id, dosage, given_by) VALUES (%s, %s, %s, %s)",
            (child_id, med_id, dosage, given_by)
        )
        cursor.execute("SELECT name FROM children WHERE child_id = %s", (child_id,))
        child_name = cursor.fetchone()[0]
        cursor.execute("SELECT name FROM medications WHERE medication_id = %s", (med_id,))
        med_name = cursor.fetchone()[0]
        cursor.execute("SELECT p.line_id FROM parents p JOIN children c ON p.parent_id = c.parent_id WHERE c.child_id = %s", (child_id,))
        line_id = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()
        return {"child_name": child_name, "med_name": med_name, "line_id": line_id}
    return None

def get_parent_line_id(child_id):
    db = get_db()
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT p.line_id FROM parents p JOIN children c ON p.parent_id = c.parent_id WHERE c.child_id = %s", (child_id,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result[0] if result else None
    return None

def get_schedules():
    db = get_db()
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT event_date, event_name FROM schedules")
        result = {row[0].strftime("%Y-%m-%d"): row[1] for row in cursor.fetchall()}
        cursor.close()
        db.close()
        return result
    return {}

def add_schedule(date, event):
    db = get_db()
    if db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO schedules (event_name, event_date) VALUES (%s, %s)", (event, date))
        db.commit()
        cursor.close()
        db.close()
        return get_schedules()
    return {}

'''
from config.firebase_config import db

#-----------------데이터베이스 읽기---------------------#


# 문서 선택 및 가져오기
#document_ref = db.document("test_name")
#doc = document_ref.get()

#데이터 읽기
#data=ref.get()
#print(data)


def db_name():
     collection_ref = db.collection("users")
     names = [doc.to_dict()["name"] for doc in collection_ref.stream()]
     return names


def db_phone():
     collection_ref = db.collection("users")
     phones = [doc.to_dict()["phone"] for doc in collection_ref.stream()]

     return phones'''