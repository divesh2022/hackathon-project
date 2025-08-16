import pyodbc
from datetime import datetime

# Database connection setup
def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost;'
        'DATABASE=sehat_sathi;'
        'Trusted_Connection=yes;'
    )

# Add a new naive user
def add_naive_user(user_id, phone, symptoms):
    query = """
    INSERT INTO NaiveUser (user_id, phone_naive, call_timestamp, symptoms)
    VALUES (?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, user_id, phone, datetime.now(), symptoms)
        conn.commit()
        print(f"✅ Naive user {user_id} added.")

# Report new symptoms for an existing user
def update_symptoms(user_id, new_symptoms):
    query = """
    UPDATE NaiveUser
    SET symptoms = ?
    WHERE user_id = ?
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, new_symptoms, user_id)
        conn.commit()
        print(f"🩺 Symptoms updated for user {user_id}.")

# Book a slot by assigning a doctor to a patient
def book_slot(doctor_id, patient_id):
    query = """
    INSERT INTO DoctorPatientAssignment (doctor_id, patient_id)
    VALUES (?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, doctor_id, patient_id)
        conn.commit()
        print(f"📅 Slot booked: Doctor {doctor_id} assigned to Patient {patient_id}.")

# View patient health summary
def get_health_summary(patient_id):
    query = """
    SELECT * FROM UserHealthSummary WHERE patient_id = ?
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, patient_id)
        row = cursor.fetchone()
        if row:
            print("🧾 Health Summary:")
            for col, val in zip([column[0] for column in cursor.description], row):
                print(f"{col}: {val}")
        else:
            print("❌ No summary found for this patient.")

# Example usage
if __name__ == "__main__":
    add_naive_user(101, "9876543210", "Fever, cough")
    update_symptoms(101, "Fever, cough, fatigue")
    book_slot(1, 101)
    get_health_summary(101)
