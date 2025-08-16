import streamlit as st
from sehat_sathi_ops import (
    add_naive_user,
    update_symptoms,
    book_slot,
    get_health_summary
)

st.title("🩺 Sehat Sathi Dashboard")

operation = st.sidebar.selectbox("Choose Operation", [
    "Add New User", "Report Symptoms", "Book Slot", "View Health Summary"
])

if operation == "Add New User":
    st.subheader("➕ Add New Naive User")
    user_id = st.number_input("User ID", min_value=1)
    phone = st.text_input("Phone Number")
    symptoms = st.text_area("Symptoms")
    if st.button("Add User"):
        add_naive_user(user_id, phone, symptoms)
        st.success(f"User {user_id} added successfully.")

elif operation == "Report Symptoms":
    st.subheader("📝 Update Symptoms")
    user_id = st.number_input("User ID", min_value=1)
    new_symptoms = st.text_area("New Symptoms")
    if st.button("Update Symptoms"):
        update_symptoms(user_id, new_symptoms)
        st.success(f"Symptoms updated for user {user_id}.")

elif operation == "Book Slot":
    st.subheader("📅 Book Doctor Slot")
    doctor_id = st.number_input("Doctor ID", min_value=1)
    patient_id = st.number_input("Patient ID", min_value=1)
    if st.button("Book Slot"):
        book_slot(doctor_id, patient_id)
        st.success(f"Doctor {doctor_id} assigned to Patient {patient_id}.")

elif operation == "View Health Summary":
    st.subheader("📋 Patient Health Summary")
    patient_id = st.number_input("Patient ID", min_value=1)
    if st.button("Fetch Summary"):
        summary = get_health_summary(patient_id)
        if summary:
            for key, value in summary.items():
                st.write(f"**{key}**: {value}")
        else:
            st.warning("No summary found for this patient.")
