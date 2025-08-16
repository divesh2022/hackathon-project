-- ============================
-- TRIGGERS FOR DATABASE
-- ============================

--  Escalate patient to doctor if urgency is Yellow or Red
CREATE TRIGGER trg_escalate_patient
ON Patient
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO DoctorPatientAssignment (doctor_id, patient_id)
    SELECT TOP 1 D.doctor_id, I.patient_id
    FROM inserted I
    JOIN Doctor D ON D.availability_status = 1
    WHERE I.urgency_level IN ('Red', 'Yellow');
END;
GO

--  Send SMS notification when a new patient is registered
CREATE TRIGGER trg_notify_patient_sms
ON Patient
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO SMSNotification (recipient_phone, message, created_at)
    SELECT 
        I.phone_patient,
        'Welcome! Your case has been registered with urgency level: ' + I.urgency_level,
        GETDATE()
    FROM inserted I;
END;
GO

--  Auto-generate prescription summary placeholder after doctor assignment
CREATE TRIGGER trg_generate_prescription_summary
ON DoctorPatientAssignment
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Prescription (patient_id, summary)
    SELECT 
        I.patient_id,
        'Prescription summary pending. Please update after consultation.'
    FROM inserted I;
END;
GO

--  Audit urgency downgrade from Red/Yellow to Blue
CREATE TRIGGER trg_audit_urgency_change
ON Patient
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO AuditLog (patient_id, old_level, new_level, created_at, reason)
    SELECT 
        D.patient_id,
        D.urgency_level,
        I.urgency_level,
        GETDATE(),
        'Manual downgrade — verify AI classification'
    FROM deleted D
    JOIN inserted I ON D.patient_id = I.patient_id
    WHERE D.urgency_level IN ('Red', 'Yellow') AND I.urgency_level = 'Blue';
END;
GO

--  Request feedback after doctor–patient assignment
CREATE TRIGGER trg_request_feedback
ON DoctorPatientAssignment
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Feedback (patient_id, rating, created_at)
    SELECT 
        I.patient_id,
        NULL,
        GETDATE()
    FROM inserted I;
END;
GO
