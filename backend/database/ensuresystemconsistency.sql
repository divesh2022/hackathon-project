CREATE PROCEDURE EnsureSystemConsistency
    @phone_no VARCHAR(15),
    @name_of_patient VARCHAR(100),
    @urgency_level VARCHAR(10),
    @location VARCHAR(100),
    @problem_reported VARCHAR(MAX),
    @advice_given VARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @patient_id INT;
    SELECT @patient_id = patient_id FROM Patient
    WHERE name_patient = @name_of_patient AND phone_patient = @phone_no;

    IF @patient_id IS NULL
    BEGIN
        RAISERROR('Patient record not found.', 16, 1);
        RETURN;
    END

    -- Log AI response
    INSERT INTO AIResponseLog (timestamp, phone_no, urgency_level, location, name_of_caller, name_of_patient, problem_reported, advice_given)
    VALUES (GETDATE(), @phone_no, @urgency_level, @location, @name_of_patient, @name_of_patient, @problem_reported, @advice_given);

    -- Log symptom analysis
    DECLARE @user_id INT;
    SELECT @user_id = user_id FROM NaiveUser WHERE phone_naive = @phone_no;

    IF @user_id IS NOT NULL
    BEGIN
        INSERT INTO SymptomAnalysisLog (user_id, symptoms, assigned_level, model_version, timestamp)
        VALUES (@user_id, @problem_reported, @urgency_level, 'v1.2.3', GETDATE());
    END

    -- Allocate resources based on urgency
    IF @urgency_level = 'Red'
    BEGIN
        INSERT INTO HospitalResponse (staff_id, patient_id)
        SELECT TOP 1 staff_id, @patient_id FROM HospitalStaff WHERE hospital_name LIKE '%' + @location + '%';

        INSERT INTO SMSNotification (recipient_phone, message)
        VALUES (@phone_no, 'Emergency alert: Hospital team notified.');

        INSERT INTO AuditLog (patient_id, old_level, new_level, created_at, reason)
        VALUES (@patient_id, 'Unknown', 'Red', GETDATE(), 'AI classified as emergency');
    END
    ELSE IF @urgency_level = 'Yellow'
    BEGIN
        INSERT INTO DoctorPatientAssignment (doctor_id, patient_id)
        SELECT TOP 1 doctor_id, @patient_id FROM Doctor WHERE availability_status = 1;

        INSERT INTO SMSNotification (recipient_phone, message)
        VALUES (@phone_no, 'Doctor assigned. Expect a call soon.');

        INSERT INTO AuditLog (patient_id, old_level, new_level, created_at, reason)
        VALUES (@patient_id, 'Unknown', 'Yellow', GETDATE(), 'AI classified as moderate');
    END
    ELSE IF @urgency_level = 'Blue'
    BEGIN
        INSERT INTO ASHA_Assignments (asha_id, patient_id)
        SELECT TOP 1 asha_id, @patient_id FROM ASHAWorker WHERE region = @location;

        INSERT INTO SMSNotification (recipient_phone, message)
        VALUES (@phone_no, 'ASHA worker will visit you soon.');

        INSERT INTO AuditLog (patient_id, old_level, new_level, created_at, reason)
        VALUES (@patient_id, 'Unknown', 'Blue', GETDATE(), 'AI classified as mild');
    END
END;
