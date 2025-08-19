-- Doctors
INSERT INTO UserLogin (role_name, user_id, phone_number)
SELECT 'Doctor', doctor_id, phone_doctor FROM Doctor;

-- ASHA Workers
INSERT INTO UserLogin (role_name, user_id, phone_number)
SELECT 'ASHAWorker', asha_id, phone_asha FROM ASHAWorker;

-- Patients
INSERT INTO UserLogin (role_name, user_id, phone_number)
SELECT 'Patient', patient_id, phone_patient FROM Patient;

-- Naive Users
INSERT INTO UserLogin (role_name, user_id, phone_number)
SELECT 'NaiveUser', user_id, phone_naive FROM NaiveUser;

-- Caregivers
INSERT INTO UserLogin (role_name, user_id, phone_number)
SELECT 'Caregiver', caregiver_id, phone_caregiver FROM Caregiver;

-- Call Center Operators
INSERT INTO UserLogin (role_name, user_id, phone_number)
SELECT 'CallCenterOperator', operator_id, phone_operator FROM CallCenterOperator;

-- Hospital Staff
INSERT INTO UserLogin (role_name, user_id, phone_number)
SELECT 'HospitalStaff', staff_id, phone_staff FROM HospitalStaff;

-- Admins
INSERT INTO UserLogin (role_name, user_id, phone_number)
SELECT 'Admin', admin_id, phone_admin FROM Admin;
