# auth_admin.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import api  # assumes api.connect_to_database() is defined

router = APIRouter()
conn = api.connect_to_database()

# 📦 Pydantic model for admin actions
class AdminAction(BaseModel):
    action: str  # "read", "insert", "update", "delete"
    table_name: str
    data: dict = None
    condition: str = None

# 🔧 Admin endpoint
@router.post("/admin")
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
        if not action.data:
            raise HTTPException(status_code=400, detail="Missing data for insert.")
        columns = ', '.join(action.data.keys())
        placeholders = ', '.join(['?'] * len(action.data))
        values = tuple(action.data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
        return {"status": "success", "message": "Record inserted successfully."}

    elif action.action == "update":
        if not action.data or not action.condition:
            raise HTTPException(status_code=400, detail="Missing data or condition for update.")
        set_clause = ', '.join([f"{k} = ?" for k in action.data.keys()])
        values = tuple(action.data.values())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {action.condition}"
        cursor.execute(query, values)
        conn.commit()
        return {"status": "success", "message": "Record updated successfully."}

    elif action.action == "delete":
        if not action.condition:
            raise HTTPException(status_code=400, detail="Missing condition for delete.")
        query = f"DELETE FROM {table_name} WHERE {action.condition}"
        cursor.execute(query)
        conn.commit()
        return {"status": "success", "message": "Record deleted successfully."}

    else:
        raise HTTPException(status_code=400, detail="Invalid action.")
# Register the router with the main FastAPI app
'''
# auth.py

from fastapi import FastAPI
from auth_admin import router as admin_router

app = FastAPI()

# Include admin routes
app.include_router(admin_router)

'''
