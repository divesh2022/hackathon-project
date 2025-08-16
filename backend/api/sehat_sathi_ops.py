import pyodbc
from datetime import datetime

def get_connection():
    return pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=sehat_sathi;"
    "Trusted_Connection=yes;"
)

# ============================
# USER OPERATIONS
# ============================

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

# ============================
# PATIENT HEALTH OPERATIONS
# ============================

def update_medical_history(patient_id, new_entry):
    query = """
    UPDATE Patient
    SET medical_history = COALESCE(medical_history, '') + CHAR(13) + CHAR(10) + ?
    WHERE patient_id = ?
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, new_entry, patient_id)
        conn.commit()

def add_prescription(patient_id, summary):
    query = """
    INSERT INTO Prescription (patient_id, summary)
    VALUES (?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, patient_id, summary)
        conn.commit()

def log_urgency_change(patient_id, old_level, new_level, reason):
    query = """
    INSERT INTO AuditLog (patient_id, old_level, new_level, reason)
    VALUES (?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, patient_id, old_level, new_level, reason)
        conn.commit()

def get_health_summary(patient_id):
    query = "SELECT * FROM Patient WHERE patient_id = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, patient_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        return None
