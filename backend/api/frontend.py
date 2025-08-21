# user_dashboard.py

import streamlit as st
import requests
import pandas as pd
import api  # assumes api.connect_to_database() is defined

conn = api.connect_to_database()
cursor = conn.cursor()

st.set_page_config(page_title="Sehat Sathi Portal", layout="wide")
st.title("🔐 Sehat Sathi Unified Login")

# Session state for login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.user_id = None

# ============================
# 🔐 Login Section
# ============================
if not st.session_state.authenticated:
    role_name = st.selectbox("Role", ["Admin", "Doctor", "ASHAWorker", "HospitalStaff", "CallCenterOperator","Patient"])
    user_id = st.text_input("User ID")
    phone_number = st.text_input("Phone Number")

    if st.button("Login"):
        payload = {
            "role_name": role_name,
            "user_id": user_id,
            "phone_number": phone_number
        }
        try:
            response = requests.post("http://localhost:8000/authenticate", json=payload)
            result = response.json()
            if result["status"] == "success":
                st.session_state.authenticated = True
                st.session_state.role = role_name
                st.session_state.user_id = user_id
                st.rerun()  # 🔁 Refresh to show dashboard
            else:
                st.error("❌ Invalid credentials.")
        except Exception as e:
            st.error(f"⚠️ Could not connect to backend: {e}")

    # No need for st.stop() here — let the app continue
    #st.stop()

# ============================
# 🎯 Role-Based Dashboard
# ============================
role = st.session_state.role
user_id = st.session_state.user_id

if role == "Admin":
    st.header("🛠️ Admin Dashboard")

    table_name = st.selectbox("Select a table", [
        "Patient", "Doctor", "ASHAWorker", "Caregiver", "CallCenterOperator",
        "HospitalStaff", "Admin", "NaiveUser", "Prescription", "Feedback", "AuditLog"
    ])
    operation = st.radio("Choose operation", ["Read", "Insert", "Update", "Delete"])

    def get_columns(table):
        cursor.execute(f"SELECT TOP 1 * FROM {table}")
        return [column[0] for column in cursor.description]

    columns = get_columns(table_name)

    if operation == "Read":
        st.subheader(f"📄 Viewing all records from `{table_name}`")
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        df = pd.DataFrame.from_records(rows, columns=columns)
        st.dataframe(df)

    elif operation == "Insert":
        st.subheader(f"➕ Insert into `{table_name}`")
        data = {}
        for col in columns:
            data[col] = st.text_input(f"{col}", key=f"insert_{col}")
        if st.button("Insert Record"):
            keys = ', '.join(data.keys())
            placeholders = ', '.join(['?'] * len(data))
            values = tuple(data.values())
            query = f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})"
            cursor.execute(query, values)
            conn.commit()
            st.success("✅ Record inserted successfully.")

    elif operation == "Update":
        st.subheader(f"✏️ Update `{table_name}`")
        condition = st.text_input("Enter WHERE condition (e.g., patient_id = 1)")
        data = {}
        for col in columns:
            data[col] = st.text_input(f"New value for {col}", key=f"update_{col}")
        if st.button("Update Record"):
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            values = tuple(data.values())
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            cursor.execute(query, values)
            conn.commit()
            st.success("✅ Record updated successfully.")

    elif operation == "Delete":
        st.subheader(f"🗑️ Delete from `{table_name}`")
        condition = st.text_input("Enter WHERE condition (e.g., doctor_id = 2)")
        if st.button("Delete Record"):
            query = f"DELETE FROM {table_name} WHERE {condition}"
            cursor.execute(query)
            conn.commit()
            st.warning("⚠️ Record deleted.")

elif role == "Doctor":
    st.header("👨‍⚕️ Doctor Dashboard")

    BASE_URL = "http://localhost:8000"
    doctor_id = st.session_state.user_id

    # 1️⃣ Assigned Patients
    st.subheader("🧍 Assigned Patients")
    res = requests.get(f"{BASE_URL}/doctor/assigned/{doctor_id}")
    if res.ok:
        patients = res.json()
        st.write(f"Total Assigned: {len(patients)}")
        st.dataframe(patients)
    else:
        st.error("Failed to fetch assigned patients")

    # 2️⃣ Dashboard Analytics
    st.subheader("📊 Dashboard Analytics")
    res = requests.get(f"{BASE_URL}/doctor/dashboard/{doctor_id}")
    if res.ok:
        data = res.json()
        st.metric("Patients Treated", data["patients_treated"])
        avg = data["average_feedback"]
        st.metric("Average Feedback", round(avg, 2) if avg else "N/A")
        st.write("Urgency Logs")
        st.json(data["urgency_logs"])
    else:
        st.error("Failed to fetch dashboard data")

    # 3️⃣ Risk Alerts
    st.subheader("⚠️ Risk Alerts")
    res = requests.get(f"{BASE_URL}/doctor/risk-alerts/{doctor_id}")
    if res.ok:
        alerts = res.json()["risk_patients"]
        if alerts:
            st.warning(f"Patients with Red/Yellow alerts: {alerts}")
        else:
            st.success("No urgent cases detected")
    else:
        st.error("Failed to fetch risk alerts")

    # 4️⃣ AI Diagnosis History
    st.subheader("🤖 AI Diagnosis History")
    res = requests.get(f"{BASE_URL}/doctor/ai-diagnosis/{doctor_id}")
    if res.ok:
        st.json(res.json())
    else:
        st.error("Failed to fetch AI diagnosis data")


elif role == "ASHAWorker":
    st.header("🧕 ASHA Worker Dashboard")
    st.info("🚧 This section is under construction. Visit logging and patient tracking features will be added here.")

elif role == "HospitalStaff":
    st.header("🏥 Hospital Staff Dashboard")
    st.info("🚧 Emergency logging and patient response tools will be added here.")

elif role == "CallCenterOperator":
    st.header("☎️ Call Center Operator Dashboard")
    st.info("🚧 Naive user triage and SMS notification tools will be added here.")
elif role == "Patient":
    st.header("👤 Patient Dashboard")

    BASE_URL = "http://localhost:8000"
    patient_id = st.session_state.user_id
    phone = st.text_input("📱 Confirm your Phone Number", value="")

    if not phone:
        st.warning("Please enter your phone number to view SMS notifications.")
    else:
        # 1️⃣ Patient Record
        st.subheader("📄 Patient Record")
        res = requests.get(f"{BASE_URL}/patient/{patient_id}")
        st.json(res.json())

        # 2️⃣ Feedback Submission
        st.subheader("📝 Submit Feedback")
        rating = st.slider("Rate your experience", 1, 5)
        if st.button("Submit Feedback"):
            feedback = {"patient_id": int(patient_id), "rating": rating}
            res = requests.post(f"{BASE_URL}/patient/feedback", json=feedback)
            st.success(res.json()["message"])

        # 3️⃣ SMS Notifications
        st.subheader("📲 SMS Notifications")
        res = requests.get(f"{BASE_URL}/patient/sms/{phone}")
        st.json(res.json())

        # 4️⃣ Prescription Summary
        st.subheader("💊 Prescription Summary")
        res = requests.get(f"{BASE_URL}/patient/prescriptions/{patient_id}")
        st.json(res.json())

        # 5️⃣ Assigned Doctor Details
        st.subheader("👨‍⚕️ Assigned Doctor")
        res = requests.get(f"{BASE_URL}/patient/doctor/{patient_id}")
        st.json(res.json())

        # 6️⃣ Health Summary
        st.subheader("🧠 Health Summary")
        res = requests.get(f"{BASE_URL}/patient/health-summary/{patient_id}")
        st.json(res.json())

        # 7️⃣ Hospital Details
        st.subheader("🏥 Hospital Staff Assigned")
        res = requests.get(f"{BASE_URL}/patient/hospital/{patient_id}")
        st.json(res.json())

        # 8️⃣ AI Response Log
        st.subheader("🤖 AI Diagnosis Log")
        res = requests.get(f"{BASE_URL}/patient/ai-response/{patient_id}")
        st.json(res.json())

else:
    st.error("❌ Unknown role. Please contact system administrator.")




