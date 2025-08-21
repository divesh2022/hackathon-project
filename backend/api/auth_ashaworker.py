# auth_ashaworker.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import api  # assumes api.connect_to_database() is defined

router = APIRouter(prefix="/asha", tags=["ASHA Worker"])
conn = api.connect_to_database()

# -------------------- Schemas --------------------

class VisitNote(BaseModel):
    asha_id: int
    patient_id: int
    notes: str

# -------------------- 1️⃣ Read Assigned Patients --------------------

@router.get("/assigned/{asha_id}", response_model=List[Dict[str, Any]])
def get_assigned_patients(asha_id: int):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT patient_id FROM ASHA_Assignments WHERE asha_id = ?",
            (asha_id,)
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching assigned patients: {str(e)}")

# -------------------- 2️⃣ Insert Visit Notes --------------------

@router.post("/visit-log")
def insert_visit_log(data: VisitNote):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO VisitLog (asha_id, patient_id, notes) VALUES (?, ?, ?)",
            (data.asha_id, data.patient_id, data.notes)
        )
        conn.commit()
        return {"status": "success", "message": "Visit note recorded."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting visit log: {str(e)}")

# -------------------- 3️⃣ Access Medical History --------------------

@router.get("/medical-history/{patient_id}", response_model=Dict[str, Any])
def get_medical_history(patient_id: int):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT urgency_level, medical_history FROM Patient WHERE patient_id = ?",
            (patient_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Patient not found.")
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching medical history: {str(e)}")
