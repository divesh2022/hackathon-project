import streamlit as st
import requests

st.set_page_config(page_title="Sehat Sathi Portal", page_icon="🩺")

# ============================
# 🔐 Login Page
# ============================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_id = None

if not st.session_state.logged_in:
    st.title("🔐 Sehat Sathi Login")

    role = st.selectbox("Select your role", [
        "Admin", "Patient", "Doctor", "ASHAWorker", "Caregiver",
        "CallCenterOperator", "HospitalStaff", "NaiveUser"
    ])
    user_id = st.text_input("Enter your User ID")
    phone_number = st.text_input("Enter your Phone Number")

    if st.button("Login"):
        if not user_id or not phone_number:
            st.warning("Please fill in all fields.")
        else:
            payload = {
                "role_name": role,
                "user_id": user_id,
                "phone_number": phone_number
            }
            try:
                response = requests.post("http://localhost:8000/authenticate", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    if data["status"] in ["success", "new"]:
                        st.session_state.logged_in = True
                        st.session_state.role = data["role"]
                        st.session_state.user_id = user_id
                        st.success(data["message"])
                        st.rerun()
                    else:
                        st.error("Unexpected response.")
                else:
                    st.error(response.json()["detail"])
            except Exception as e:
                st.error(f"Connection error: {e}")

# ============================
# 🧑‍⚕️ Role-Specific Panels
# ============================

else:
    st.sidebar.success(f"Logged in as {st.session_state.role}")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({
    "logged_in": False,
    "role": None,
    "user_id": None
}))
    st.sidebar.markdown("---")

    role = st.session_state.role
    user_id = st.session_state.user_id

    st.title(f"🩺 {role} Dashboard")

    if role == "Doctor":
        st.subheader("Assigned Patients")
        try:
            res = requests.get(f"http://localhost:8000/doctor/patients/{user_id}")
            st.json(res.json())
        except:
            st.error("Failed to fetch patient data.")

        st.subheader("Update Availability")
        status = st.checkbox("Available")
        if st.button("Update Status"):
            requests.put("http://localhost:8000/doctor/availability", json={
                "doctor_id": int(user_id),
                "status": status
            })
            st.success("Availability updated.")

    elif role == "ASHAWorker":
        st.subheader("Assigned Patients")
        try:
            res = requests.get(f"http://localhost:8000/asha/patients/{user_id}")
            st.json(res.json())
        except:
            st.error("Failed to fetch ASHA assignments.")

    elif role == "Patient":
        st.subheader("Your Record")
        try:
            res = requests.get(f"http://localhost:8000/patient/{user_id}")
            st.json(res.json())
        except:
            st.error("Failed to fetch patient record.")

        st.subheader("Submit Feedback")
        rating = st.slider("Rate your experience", 1, 5)
        if st.button("Submit Feedback"):
            requests.post("http://localhost:8000/patient/feedback", json={
                "patient_id": int(user_id),
                "rating": rating
            })
            st.success("Feedback submitted.")

    elif role == "CallCenterOperator":
        st.subheader("Naive User Symptoms")
        try:
            res = requests.get("http://localhost:8000/operator/naive-users")
            st.json(res.json())
        except:
            st.error("Failed to fetch NaiveUser data.")

    elif role == "HospitalStaff":
        st.subheader("Hospital Patient Data")
        try:
            res = requests.get(f"http://localhost:8000/hospital/patients/{user_id}")
            st.json(res.json())
        except:
            st.error("Failed to fetch hospital patient data.")

    elif role == "Caregiver":
        st.subheader("Assigned Patients")
        try:
            res = requests.get(f"http://localhost:8000/caregiver/patients/{user_id}")
            st.json(res.json())
        except:
            st.error("Failed to fetch caregiver data.")

    elif role == "NaiveUser":
        st.subheader("Welcome New User")
        st.info("Your symptoms will be recorded by a CallCenter Operator shortly.")

    elif role == "Admin":
        st.subheader("Admin Panel")
        st.info("Use external tools or APIs to manage database records.")

# ============================
