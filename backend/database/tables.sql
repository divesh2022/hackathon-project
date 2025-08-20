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
    urgency_level VARCHAR(10),
    medical_history VARCHAR(MAX)
);

CREATE TABLE NaiveUser (
    user_id INT PRIMARY KEY,
    phone_naive VARCHAR(15),
    call_timestamp DATETIME,
    symptoms VARCHAR(MAX)
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
CREATE TABLE SMSNotification (
    notification_id INT IDENTITY PRIMARY KEY,
    recipient_phone VARCHAR(15),
    message VARCHAR(255),
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE Prescription (
    prescription_id INT IDENTITY PRIMARY KEY,
    patient_id INT,
    summary VARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE AuditLog (
    log_id INT IDENTITY PRIMARY KEY,
    patient_id INT,
    old_level VARCHAR(10),
    new_level VARCHAR(10),
    created_at DATETIME DEFAULT GETDATE(),
    reason VARCHAR(255)
);

CREATE TABLE Feedback (
    feedback_id INT IDENTITY PRIMARY KEY,
    patient_id INT,
    rating INT,
    created_at DATETIME DEFAULT GETDATE()
);
-- 1. VisitLog: ASHA Worker offline visits
CREATE TABLE VisitLog (
    visit_id INT IDENTITY PRIMARY KEY,
    asha_id INT,
    patient_id INT,
    visit_date DATETIME DEFAULT GETDATE(),
    notes VARCHAR(MAX),
    offline_mode BIT DEFAULT 1,
    FOREIGN KEY (asha_id) REFERENCES ASHAWorker(asha_id),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);

-- 2. MedicationReminder: SMS/voice reminders for medicine
CREATE TABLE MedicationReminder (
    reminder_id INT IDENTITY PRIMARY KEY,
    patient_id INT,
    message VARCHAR(255),
    scheduled_time DATETIME,
    status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);

-- 3. VoiceTipLibrary: Rotating hygiene tips for call queue
CREATE TABLE VoiceTipLibrary (
    tip_id INT IDENTITY PRIMARY KEY,
    language VARCHAR(50),
    topic VARCHAR(100),
    audio_file_path VARCHAR(255),
    last_used DATETIME
);

-- 4. DiseaseAlert: SMS-based health alerts
CREATE TABLE DiseaseAlert (
    alert_id INT IDENTITY PRIMARY KEY,
    region VARCHAR(100),
    disease_name VARCHAR(100),
    message VARCHAR(255),
    created_at DATETIME DEFAULT GETDATE()
);

-- 5. SymptomAnalysisLog: AI classification of urgency level
CREATE TABLE SymptomAnalysisLog (
    analysis_id INT IDENTITY PRIMARY KEY,
    user_id INT,
    symptoms VARCHAR(MAX),
    assigned_level VARCHAR(10),
    model_version VARCHAR(50),
    timestamp DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES NaiveUser(user_id)
);

-- 6. ImageDiagnosis: AI-based skin disease detection
CREATE TABLE ImageDiagnosis (
    image_id INT IDENTITY PRIMARY KEY,
    patient_id INT,
    image_path VARCHAR(255),
    diagnosis VARCHAR(100),
    confidence_score FLOAT,
    timestamp DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);

-- 7. PrescriptionSummary: AI-generated summary of doctor prescriptions
CREATE TABLE PrescriptionSummary (
    summary_id INT IDENTITY PRIMARY KEY,
    prescription_id INT,
    dosage VARCHAR(100),
    instructions VARCHAR(MAX),
    side_effects VARCHAR(MAX),
    FOREIGN KEY (prescription_id) REFERENCES Prescription(prescription_id)
);

-- 8. LanguagePreference: Multi-language support for users
CREATE TABLE LanguagePreference (
    user_id INT PRIMARY KEY,
    preferred_language VARCHAR(50),
    region VARCHAR(100),
    accent_notes VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES NaiveUser(user_id)
);
