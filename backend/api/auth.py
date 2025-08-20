from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
import api
import pandas as pd

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Sehat Sathi API is running!"}
conn = api.connect_to_database()

# Role-to-table mapping
role_table_map = {
    "Patient": "Patient",
    "Doctor": "Doctor",
    "ASHAWorker": "ASHAWorker",
    "Caregiver": "Caregiver",
    "CallCenterOperator": "CallCenterOperator",
    "HospitalStaff": "HospitalStaff",
    "Admin": "Admin",
    "NaiveUser": "NaiveUser"
}

# Models
class AuthRequest(BaseModel):
    role_name: str
    user_id: str
    phone_number: str

class AdminAction(BaseModel):
    action: str
    table_name: str
    data: dict = None
    condition: str = None
class IDModel(BaseModel):
    id: int

class PrescriptionModel(BaseModel):
    patient_id: int
    summary: str

class AvailabilityModel(BaseModel):
    doctor_id: int
    status: bool

class VisitNoteModel(BaseModel):
    patient_id: int
    old_level: str
    new_level: str
    reason: str

class FeedbackModel(BaseModel):
    patient_id: int
    rating: int

class SMSModel(BaseModel):
    phone: str
    message: str

class CallAssistanceModel(BaseModel):
    operator_id: int
    user_id: int

class UrgencyModel(BaseModel):
    patient_id: int
    level: str

class StaffUpdateModel(BaseModel):
    staff_id: int
    role: str
    hospital: str

class NaiveUserModel(BaseModel):
    user_id: int
    phone: str
    timestamp: str
    symptoms: str

class AIResponseModel(BaseModel):
    patient_id: int
    caller_info: str
    symptoms: str
    advice: str

# Authentication endpoint
@app.post("/authenticate")
def authenticate_user(auth: AuthRequest):
    role_name = auth.role_name
    user_id = auth.user_id
    phone_number = auth.phone_number

    if role_name not in role_table_map:
        raise HTTPException(status_code=400, detail="Invalid role selected.")

    table = role_table_map[role_name]
    id_column = f"{role_name.lower()}_id"
    phone_column = "phone_" + role_name.lower()

    query = f"""
        SELECT * FROM {table}
        WHERE {id_column} = ? AND {phone_column} = ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (user_id, phone_number))
    result = cursor.fetchone()

    if result:
        return {"status": "success", "message": "Welcome back!", "role": role_name}
    elif role_name == "NaiveUser":
        return {"status": "new", "message": "Welcome! You’re new here."}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

# Admin API endpoint
@app.post("/admin")
def admin_api(action: AdminAction):
    cursor = conn.cursor()
    table_name = action.table_name

    if action.action == "read":
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        df = pd.DataFrame.from_records(rows, columns=columns)
        return df.to_dict(orient="records")

    elif action.action == "insert":
        columns = ', '.join(action.data.keys())
        placeholders = ', '.join(['?'] * len(action.data))
        values = tuple(action.data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
        return {"status": "success", "message": "Record inserted successfully."}

    elif action.action == "update":
        set_clause = ', '.join([f"{k} = ?" for k in action.data.keys()])
        values = tuple(action.data.values())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {action.condition}"
        cursor.execute(query, values)
        conn.commit()
        return {"status": "success", "message": "Record updated successfully."}

    elif action.action == "delete":
        query = f"DELETE FROM {table_name} WHERE {action.condition}"
        cursor.execute(query)
        conn.commit()
        return {"status": "success", "message": "Record deleted successfully."}

    raise HTTPException(status_code=400, detail="Invalid action.")
# ============================
# 🧑‍⚕️ Doctor Endpoints
# ============================

@app.get("/doctor/patients/{doctor_id}")
def get_assigned_patients(doctor_id: int):
    query = """
        SELECT p.* FROM Patient p
        JOIN DoctorPatientAssignment dpa ON p.patient_id = dpa.patient_id
        WHERE dpa.doctor_id = ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (doctor_id,))
    return cursor.fetchall()

@app.post("/doctor/prescription")
def insert_prescription(data: PrescriptionModel):
    query = "INSERT INTO Prescription (patient_id, summary) VALUES (?, ?)"
    cursor = conn.cursor()
    cursor.execute(query, (data.patient_id, data.summary))
    conn.commit()
    return {"status": "success"}

@app.put("/doctor/availability")
def update_availability(data: AvailabilityModel):
    query = "UPDATE Doctor SET availability_status = ? WHERE doctor_id = ?"
    cursor = conn.cursor()
    cursor.execute(query, (data.status, data.doctor_id))
    conn.commit()
    return {"status": "updated"}

@app.get("/doctor/logs/{doctor_id}")
def view_patient_logs(doctor_id: int):
    query = """
        SELECT a.*, f.* FROM DoctorPatientAssignment dpa
        JOIN AuditLog a ON dpa.patient_id = a.patient_id
        JOIN Feedback f ON dpa.patient_id = f.patient_id
        WHERE dpa.doctor_id = ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (doctor_id,))
    return cursor.fetchall()
# ============================
# ============================
# 🧕 ASHA Worker Endpoints
# ============================

@app.get("/asha/patients/{asha_id}")
def get_assigned_patients_by_asha(asha_id: int):
    query = """
        SELECT p.* FROM Patient p
        JOIN ASHA_Assignments aa ON p.patient_id = aa.patient_id
        WHERE aa.asha_id = ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (asha_id,))
    return cursor.fetchall()

@app.post("/asha/visit-note")
def insert_visit_note(data: VisitNoteModel):
    query = """
        INSERT INTO AuditLog (patient_id, old_level, new_level, reason)
        VALUES (?, ?, ?, ?)
    """
    cursor = conn.cursor()
    cursor.execute(query, (data.patient_id, data.old_level, data.new_level, data.reason))
    conn.commit()
    return {"status": "logged"}

@app.get("/asha/history/{patient_id}")
def get_medical_history_offline(patient_id: int):
    query = "SELECT medical_history FROM Patient WHERE patient_id = ?"
    cursor = conn.cursor()
    cursor.execute(query, (patient_id,))
    return cursor.fetchone()
# ============================
# ============================
# 🧑‍🦱 Patient Endpoints
# ============================

@app.get("/patient/{patient_id}")
def get_patient_record(patient_id: int):
    query = "SELECT * FROM Patient WHERE patient_id = ?"
    cursor = conn.cursor()
    cursor.execute(query, (patient_id,))
    return cursor.fetchone()

@app.post("/patient/feedback")
def submit_feedback(data: FeedbackModel):
    query = "INSERT INTO Feedback (patient_id, rating) VALUES (?, ?)"
    cursor = conn.cursor()
    cursor.execute(query, (data.patient_id, data.rating))
    conn.commit()
    return {"status": "submitted"}

@app.get("/patient/sms/{phone}")
def get_sms_notifications(phone: str):
    query = "SELECT * FROM SMSNotification WHERE recipient_phone = ?"
    cursor = conn.cursor()
    cursor.execute(query, (phone,))
    return cursor.fetchall()

@app.get("/patient/prescriptions/{patient_id}")
def get_prescription_summary(patient_id: int):
    query = "SELECT summary FROM Prescription WHERE patient_id = ?"
    cursor = conn.cursor()
    cursor.execute(query, (patient_id,))
    return cursor.fetchall()
# ============================
# ============================
# ☎️ CallCenter Operator Endpoints
# ============================

@app.post("/operator/call-assist")
def insert_call_assistance(data: CallAssistanceModel):
    query = "INSERT INTO CallAssistance (operator_id, user_id) VALUES (?, ?)"
    cursor = conn.cursor()
    cursor.execute(query, (data.operator_id, data.user_id))
    conn.commit()
    return {"status": "created"}

@app.get("/operator/naive-users")
def read_naive_user_symptoms():
    query = "SELECT * FROM NaiveUser"
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

@app.put("/operator/urgency")
def update_urgency_level(data: UrgencyModel):
    query = "UPDATE Patient SET urgency_level = ? WHERE patient_id = ?"
    cursor = conn.cursor()
    cursor.execute(query, (data.level, data.patient_id))
    conn.commit()
    return {"status": "updated"}

@app.post("/operator/sms")
def trigger_sms(data: SMSModel):
    query = "INSERT INTO SMSNotification (recipient_phone, message) VALUES (?, ?)"
    cursor = conn.cursor()
    cursor.execute(query, (data.phone, data.message))
    conn.commit()
    return {"status": "sent"}
# ============================
# ============================
# 🏥 Hospital Staff Endpoints
# ============================

@app.get("/hospital/patients/{staff_id}")
def get_hospital_patients(staff_id: int):
    query = """
        SELECT p.* FROM Patient p
        JOIN HospitalResponse hr ON p.patient_id = hr.patient_id
        WHERE hr.staff_id = ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (staff_id,))
    return cursor.fetchall()

@app.post("/hospital/emergency")
def insert_emergency_log(data: VisitNoteModel):
    return insert_visit_note(data)

@app.put("/hospital/update")
def update_staff_info(data: StaffUpdateModel):
    query = "UPDATE HospitalStaff SET role_staff = ?, hospital_name = ? WHERE staff_id = ?"
    cursor = conn.cursor()
    cursor.execute(query, (data.role, data.hospital, data.staff_id))
    conn.commit()
    return {"status": "updated"}
# ============================
# ============================
# 🧑‍🦽 Caregiver Endpoints
# ============================

@app.get("/caregiver/patients/{caregiver_id}")
def get_patient_by_caregiver(caregiver_id: int):
    query = """
        SELECT p.* FROM Patient p
        JOIN Caregiver c ON p.patient_id = c.patient_ref
        WHERE c.caregiver_id = ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (caregiver_id,))
    return cursor.fetchall()

@app.post("/caregiver/feedback")
def insert_caregiver_feedback(data: FeedbackModel):
    return submit_feedback(data)

@app.get("/caregiver/sms/{phone}")
def receive_sms(phone: str):
    return get_sms_notifications(phone)
# ============================
# ============================
# 🧑 Naive User Endpoints
# ============================

@app.post("/naive-user/register")
def insert_naive_user(data: NaiveUserModel):
    query = """
        INSERT INTO NaiveUser (user_id, phone_naive, call_timestamp, symptoms)
        VALUES (?, ?, ?, ?)
    """
    cursor = conn.cursor()
    cursor.execute(query, (data.user_id, data.phone, data.timestamp, data.symptoms))
    conn.commit()
    return {"status": "registered"}

@app.post("/naive-user/call-assist")
def trigger_call_assistance(data: CallAssistanceModel):
    return insert_call_assistance(data)

@app.post("/naive-user/sms")
def notify_naive_user(data: SMSModel):
    return trigger_sms(data)
# ============================
# ============================
# 🤖 AI Endpoints
# ============================

@app.post("/ai/response")
def insert_ai_response_log(data: AIResponseModel):
    query = """
        INSERT INTO AIResponseLog (patient_id, caller_info, symptoms, advice, created_at)
        VALUES (?, ?, ?, ?, GETDATE())
    """
    cursor = conn.cursor()
    cursor.execute(query, (data.patient_id, data.caller_info, data.symptoms, data.advice))
    conn.commit()
# Utility endpoint to get column names
@app.get("/columns")
def get_columns(table_name: str = Query(...)):
    cursor = conn.cursor()
    cursor.execute(f"SELECT TOP 1 * FROM {table_name}")
    return [column[0] for column in cursor.description]
