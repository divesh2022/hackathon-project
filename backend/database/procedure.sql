CREATE PROCEDURE AllocateResourcesByUrgency
    @phone_no VARCHAR(15),
    @urgency_level VARCHAR(10),
    @location VARCHAR(100),
    @name_of_caller VARCHAR(100),
    @name_of_patient VARCHAR(100),
    @problem_reported VARCHAR(MAX),
    @advice_given VARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    -- Log AI response
    INSERT INTO AIResponseLog (timestamp, phone_no, urgency_level, location, name_of_caller, name_of_patient, problem_reported, advice_given)
    VALUES (GETDATE(), @phone_no, @urgency_level, @location, @name_of_caller, @name_of_patient, @problem_reported, @advice_given);

    DECLARE @patient_id INT;
    SELECT @patient_id = patient_id FROM Patient WHERE name_patient = @name_of_patient AND phone_patient = @phone_no;

    IF @urgency_level = 'Red'
    BEGIN
        -- Trigger hospital response
        INSERT INTO HospitalResponse (staff_id, patient_id)
        SELECT TOP 1 staff_id, @patient_id FROM HospitalStaff WHERE hospital_name LIKE '%' + @location + '%';
        
        -- Send emergency SMS
        INSERT INTO SMSNotification (recipient_phone, message)
        VALUES (@phone_no, 'Emergency alert: Hospital team notified.');
    END
    ELSE IF @urgency_level = 'Yellow'
    BEGIN
        -- Assign doctor
        INSERT INTO DoctorPatientAssignment (doctor_id, patient_id)
        SELECT TOP 1 doctor_id, @patient_id FROM Doctor WHERE availability_status = 1;

        -- Send SMS
        INSERT INTO SMSNotification (recipient_phone, message)
        VALUES (@phone_no, 'Doctor assigned. Expect a call soon.');
    END
    ELSE IF @urgency_level = 'Blue'
    BEGIN
        -- Assign ASHA worker
        INSERT INTO ASHA_Assignments (asha_id, patient_id)
        SELECT TOP 1 asha_id, @patient_id FROM ASHAWorker WHERE region = @location;

        -- Send SMS
        INSERT INTO SMSNotification (recipient_phone, message)
        VALUES (@phone_no, 'ASHA worker will visit you soon.');
    END
END;
