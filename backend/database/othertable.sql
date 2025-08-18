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
