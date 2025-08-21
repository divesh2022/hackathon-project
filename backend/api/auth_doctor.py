from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import api  # assumes api.connect_to_database() is defined

router = APIRouter(prefix="/doctor", tags=["Doctor"])
conn = api.connect_to_database()


# -------------------- Schemas --------------------

class PrescriptionCreate(BaseModel):
    patient_id: int
    summary: str


class AvailabilityUpdate(BaseModel):
    doctor_id: int
    status: bool  # True = available, False = unavailable


# -------------------- 1️⃣ Read Assigned Patients --------------------

@router.get("/assigned/{doctor_id}", response_model=List[Dict[str, Any]])
def get_assigned_patients(doctor_id: int):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT patient_id FROM DoctorPatientAssignment WHERE doctor_id = ?",
        (doctor_id,)
    )
    patient_ids = [row[0] for row in cursor.fetchall()]
    if not patient_ids:
        return []

    placeholders = ",".join(["?"] * len(patient_ids))
    query = f"SELECT * FROM Patient WHERE patient_id IN ({placeholders})"
    cursor.execute(query, patient_ids)
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


# -------------------- 2️⃣ Insert Prescription --------------------

@router.post("/prescription")
def add_prescription(data: PrescriptionCreate):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Prescription (patient_id, summary) VALUES (?, ?)",
        (data.patient_id, data.summary)
    )
    conn.commit()
    return {"status": "success", "message": "Prescription added successfully."}


# -------------------- 3️⃣ Update Availability --------------------

@router.put("/availability")
def update_availability(data: AvailabilityUpdate):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Doctor SET availability_status = ? WHERE doctor_id = ?",
        (int(data.status), data.doctor_id)
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Doctor not found.")
    conn.commit()
    return {"status": "success", "message": "Availability updated."}


# -------------------- 4️⃣ View AuditLog & Feedback --------------------

@router.get("/audit-feedback/{doctor_id}")
def get_audit_and_feedback(doctor_id: int):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT patient_id FROM DoctorPatientAssignment WHERE doctor_id = ?",
        (doctor_id,)
    )
    patient_ids = [row[0] for row in cursor.fetchall()]
    if not patient_ids:
        return {"audit_logs": [], "feedbacks": []}

    placeholders = ",".join(["?"] * len(patient_ids))

    cursor.execute(
        f"SELECT * FROM AuditLog WHERE patient_id IN ({placeholders})",
        patient_ids
    )
    audit_rows = cursor.fetchall()
    audit_cols = [col[0] for col in cursor.description]
    audit_logs = [dict(zip(audit_cols, row)) for row in audit_rows]

    cursor.execute(
        f"SELECT * FROM Feedback WHERE patient_id IN ({placeholders})",
        patient_ids
    )
    feedback_rows = cursor.fetchall()
    feedback_cols = [col[0] for col in cursor.description]
    feedbacks = [dict(zip(feedback_cols, row)) for row in feedback_rows]

    return {
        "audit_logs": audit_logs,
        "feedbacks": feedbacks
    }
