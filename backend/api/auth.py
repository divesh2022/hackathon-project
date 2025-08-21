# auth.py
import api  # assumes api.connect_to_database() is defined
from fastapi import FastAPI , HTTPException, Query
from auth_admin import router as admin_router 
from pydantic import BaseModel  
from auth_patient import router as patient_router  
from auth_doctor import router as doctor_router  
app = FastAPI()

# Include admin routes
app.include_router(admin_router)
# Include patient routes
app.include_router(patient_router)
# Include doctor routes
app.include_router(doctor_router)
# Include other routers as needed
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

# Utility endpoint to get column names
@app.get("/columns")
def get_columns(table_name: str = Query(...)):
    cursor = conn.cursor()
    cursor.execute(f"SELECT TOP 1 * FROM {table_name}")
    return [column[0] for column in cursor.description]
