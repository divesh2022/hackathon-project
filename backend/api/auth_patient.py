# auth_patient.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import api  # assumes api.connect_to_database() is defined

router = APIRouter()
conn = api.connect_to_database()

# 📦 Models
class FeedbackModel(BaseModel):
    patient_id: int
    rating: int

# ============================
# 1️⃣ Read own Patient record
# ============================
@router.get("/patient/{patient_id}")
def get_patient_record(patient_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Patient WHERE patient_id = ?", (patient_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Patient not found.")
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

# ============================
# 2️⃣ Submit Feedback
# ============================
@router.post("/patient/feedback")
def submit_feedback(data: FeedbackModel):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Feedback (patient_id, rating) VALUES (?, ?)", (data.patient_id, data.rating))
    conn.commit()
    return {"status": "success", "message": "Feedback submitted."}

# ============================
# 3️⃣ Receive SMS Notifications
# ============================
@router.get("/patient/sms/{phone}")
def get_sms_notifications(phone: str):
    cursor = conn.cursor()
    cursor.execute("SELECT message, created_at FROM SMSNotification WHERE recipient_phone = ? ORDER BY created_at DESC", (phone,))
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in rows]

# ============================
# 4️⃣ View Prescription Summary
# ============================
@router.get("/patient/prescriptions/{patient_id}")
def get_prescription_summary(patient_id: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.prescription_id, p.summary, ps.dosage, ps.instructions, ps.side_effects, p.created_at
        FROM Prescription p
        LEFT JOIN PrescriptionSummary ps ON p.prescription_id = ps.prescription_id
        WHERE p.patient_id = ?
        ORDER BY p.created_at DESC
    """, (patient_id,))
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in rows]

# ============================
# 5️⃣ View Assigned Doctor Details
# ============================
@router.get("/patient/doctor/{patient_id}")
def get_assigned_doctor(patient_id: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.doctor_id, d.name_doctor, d.specialization, d.phone_doctor, d.email_doctor
        FROM DoctorPatientAssignment da
        JOIN Doctor d ON da.doctor_id = d.doctor_id
        WHERE da.patient_id = ?
    """, (patient_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Doctor not assigned.")
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

# ============================
# 6️⃣ View User Health Summary
# ============================
@router.get("/patient/health-summary/{patient_id}")
def get_user_health_summary(patient_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT urgency_level, medical_history FROM Patient WHERE patient_id = ?", (patient_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Health summary not found.")
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

# ============================
# 7️⃣ View Hospital Details
# ============================
@router.get("/patient/hospital/{patient_id}")
def get_hospital_details(patient_id: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT hs.name_staff, hs.hospital_name, hs.role_staff, hs.phone_staff
        FROM HospitalResponse hr
        JOIN HospitalStaff hs ON hr.staff_id = hs.staff_id
        WHERE hr.patient_id = ?
    """, (patient_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Hospital staff not assigned.")
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

# ============================
# 8️⃣ View AI Response Log
# ============================
@router.get("/patient/ai-response/{patient_id}")
def get_ai_responses(patient_id: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT image_path, diagnosis, confidence_score, timestamp
        FROM ImageDiagnosis
        WHERE patient_id = ?
        ORDER BY timestamp DESC
    """, (patient_id,))
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in rows]

