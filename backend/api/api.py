import pyodbc

def connect_to_database():
    try:
        connection_string = (
            "DRIVER={SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=sehat_sathi;"
            "Trusted_Connection=yes;"
    )
        conn = pyodbc.connect(connection_string)
        print("✅ Connection successful!")
        return conn
    except Exception as e:
        print("❌ Connection failed:", e)
        return None
role_table_map = {
    "Doctor": "Doctor",
    "ASHAWorker": "ASHAWorker",
    "Patient": "Patient",
    "Admin": "Admin",
    "LabTechnician": "LabTechnician",
    "Pharmacist": "Pharmacist",
    "Receptionist": "Receptionist",
    "Nurse": "Nurse",
    "Radiologist": "Radiologist",
    "HealthInspector": "HealthInspector",
    "DataEntryOperator": "DataEntryOperator",
    "MedicalOfficer": "MedicalOfficer",
    "CommunityHealthWorker": "CommunityHealthWorker",
    "ITSupport": "ITSupport",
    "FinanceManager": "FinanceManager",
    "SuperAdmin": "SuperAdmin"
}

'''conn = connect_to_database()

if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 5 * FROM Patient")
    for row in cursor.fetchall():
        print(row)
    conn.close()'''
'''
conn = connect_to_database()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 5 * FROM Patient")
    for row in cursor.fetchall():
        print(row)
    conn.close()
'''
