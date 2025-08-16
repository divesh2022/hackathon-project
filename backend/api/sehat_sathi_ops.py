import pyodbc
from datetime import datetime

def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost;'
        'DATABASE=sehat_sathi;'
        'Trusted_Connection=yes;'
    )

def add_naive_user(user_id, phone, symptoms):
    query = """
    INSERT INTO NaiveUser (user_id, phone_naive, call_timestamp, symptoms)
    VALUES (?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, user_id, phone, datetime.now(), symptoms)
        conn.commit()

def update_symptoms(user_id, new_symptoms):
    query = "UPDATE NaiveUser SET symptoms = ? WHERE user_id = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, new_symptoms, user_id)
        conn.commit()

def book_slot(doctor_id, patient_id):
    query = "INSERT INTO DoctorPatientAssignment (doctor_id, patient_id) VALUES (?, ?)"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, doctor_id, patient_id)
        conn.commit()

def get_health_summary(patient_id):
    query = "SELECT * FROM UserHealthSummary WHERE patient_id = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, patient_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        return None
