USE sehat_sathi;
-- ============================
-- USER ENTITIES
-- ============================

CREATE TABLE Patient (
    patient_id INT PRIMARY KEY,
    name_patient VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    phone_patient VARCHAR(15),
    location VARCHAR(100),
    urgency_level VARCHAR(10), -- Consider ENUM('Blue', 'Yellow', 'Red')
    medical_history TEXT
);

CREATE TABLE NaiveUser (
    user_id INT PRIMARY KEY,
    phone_naive VARCHAR(15),
    call_timestamp DATETIME,
    symptoms TEXT
);

CREATE TABLE Caregiver (
    caregiver_id INT PRIMARY KEY,
    name_caregiver VARCHAR(100),
    relation_to_patient VARCHAR(50),
    phone_caregiver VARCHAR(15),
    patient_ref INT,
    FOREIGN KEY (patient_ref) REFERENCES Patient(patient_id)
);

CREATE TABLE CallCenterOperator (
    operator_id INT PRIMARY KEY,
    name_operator VARCHAR(100),
    shift_time VARCHAR(50),
    phone_operator VARCHAR(15)
);

CREATE TABLE Doctor (
    doctor_id INT PRIMARY KEY,
    name_doctor VARCHAR(100),
    specialization VARCHAR(50),
    phone_doctor VARCHAR(15),
    email_doctor VARCHAR(100),
    availability_status BIT
);

CREATE TABLE ASHAWorker (
    asha_id INT PRIMARY KEY,
    name_asha VARCHAR(100),
    region VARCHAR(100),
    phone_asha VARCHAR(15)
);

CREATE TABLE HospitalStaff (
    staff_id INT PRIMARY KEY,
    name_staff VARCHAR(100),
    hospital_name VARCHAR(100),
    role_staff VARCHAR(50),
    phone_staff VARCHAR(15)
);

CREATE TABLE Admin (
    admin_id INT PRIMARY KEY,
    name_admin VARCHAR(100),
    role_admin VARCHAR(50),
    email_admin VARCHAR(100),
    phone_admin VARCHAR(15)
);

-- ============================
-- RELATIONSHIP TABLES
-- ============================

CREATE TABLE CallAssistance (
    operator_id INT,
    user_id INT,
    PRIMARY KEY (operator_id, user_id),
    FOREIGN KEY (operator_id) REFERENCES CallCenterOperator(operator_id),
    FOREIGN KEY (user_id) REFERENCES NaiveUser(user_id)
);

CREATE TABLE ASHA_Assignments (
    asha_id INT,
    patient_id INT,
    PRIMARY KEY (asha_id, patient_id),
    FOREIGN KEY (asha_id) REFERENCES ASHAWorker(asha_id),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);

CREATE TABLE HospitalResponse (
    staff_id INT,
    patient_id INT,
    PRIMARY KEY (staff_id, patient_id),
    FOREIGN KEY (staff_id) REFERENCES HospitalStaff(staff_id),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);

CREATE TABLE AdminManagement (
    admin_id INT,
    entity_type VARCHAR(50), -- e.g., 'Doctor', 'ASHAWorker', etc.
    entity_id INT,
    PRIMARY KEY (admin_id, entity_type, entity_id),
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id)
);
CREATE TABLE DoctorPatientAssignment (
    doctor_id INT,
    patient_id INT,
    PRIMARY KEY (doctor_id, patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);
