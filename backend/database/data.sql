-- ============================
-- DUMMY DATASET FOR TESTING
-- ============================

-- Patients
INSERT INTO Patient VALUES
(1, 'Ravi Kumar', 45, 'Male', '9876543210', 'Sundar Nagar', 'Red', 'Diabetes, Hypertension'),
(2, 'Meena Devi', 32, 'Female', '9876543211', 'Mandi', 'Yellow', 'Asthma'),
(3, 'Amit Thakur', 27, 'Male', '9876543212', 'Kullu', 'Blue', 'None'),
(4, 'Sunita Sharma', 60, 'Female', '9876543213', 'Bilaspur', 'Red', 'Heart Disease'),
(5, 'Rajesh Rana', 50, 'Male', '9876543214', 'Hamirpur', 'Yellow', 'Arthritis');

-- Naive Users
INSERT INTO NaiveUser VALUES
(1, '9876543215', '2025-08-16 07:00:00', 'Fever, cough'),
(2, '9876543216', '2025-08-16 07:05:00', 'Chest pain'),
(3, '9876543217', '2025-08-16 07:10:00', 'Skin rash'),
(4, '9876543218', '2025-08-16 07:15:00', 'Headache'),
(5, '9876543219', '2025-08-16 07:20:00', 'Shortness of breath');

-- Caregivers
INSERT INTO Caregiver VALUES
(1, 'Anita Kumari', 'Wife', '9876543220', 1),
(2, 'Ramesh Singh', 'Son', '9876543221', 2),
(3, 'Geeta Devi', 'Daughter', '9876543222', 3),
(4, 'Mohit Rana', 'Brother', '9876543223', 4),
(5, 'Kiran Bala', 'Wife', '9876543224', 5);

-- Call Center Operators
INSERT INTO CallCenterOperator VALUES
(1, 'Suresh Verma', 'Morning', '9876543225'),
(2, 'Neha Joshi', 'Evening', '9876543226'),
(3, 'Pankaj Mehta', 'Night', '9876543227'),
(4, 'Divya Chauhan', 'Morning', '9876543228'),
(5, 'Aman Gupta', 'Evening', '9876543229');

-- Doctors
INSERT INTO Doctor VALUES
(1, 'Dr. Arvind', 'Cardiology', '9876543230', 'arvind@hospital.com', 1),
(2, 'Dr. Sneha', 'Pulmonology', '9876543231', 'sneha@hospital.com', 1),
(3, 'Dr. Rohan', 'Dermatology', '9876543232', 'rohan@hospital.com', 0),
(4, 'Dr. Priya', 'General Medicine', '9876543233', 'priya@hospital.com', 1),
(5, 'Dr. Vikram', 'Orthopedics', '9876543234', 'vikram@hospital.com', 0);

-- ASHA Workers
INSERT INTO ASHAWorker VALUES
(1, 'Kamla Devi', 'Sundar Nagar', '9876543235'),
(2, 'Rekha Thakur', 'Mandi', '9876543236'),
(3, 'Pooja Sharma', 'Kullu', '9876543237'),
(4, 'Sarita Verma', 'Bilaspur', '9876543238'),
(5, 'Nisha Chauhan', 'Hamirpur', '9876543239');

-- Hospital Staff
INSERT INTO HospitalStaff VALUES
(1, 'Manoj Kumar', 'Civil Hospital SN', 'Nurse', '9876543240'),
(2, 'Anjali Mehta', 'District Hospital Mandi', 'Technician', '9876543241'),
(3, 'Ravi Sharma', 'Kullu Hospital', 'Doctor', '9876543242'),
(4, 'Deepika Rana', 'Bilaspur Hospital', 'Receptionist', '9876543243'),
(5, 'Vikas Chauhan', 'Hamirpur Hospital', 'Paramedic', '9876543244');

-- Admins
INSERT INTO Admin VALUES
(1, 'Admin1', 'SuperAdmin', 'admin1@helpline.com', '9876543245'),
(2, 'Admin2', 'DataManager', 'admin2@helpline.com', '9876543246'),
(3, 'Admin3', 'OpsLead', 'admin3@helpline.com', '9876543247'),
(4, 'Admin4', 'TechSupport', 'admin4@helpline.com', '9876543248'),
(5, 'Admin5', 'FieldCoordinator', 'admin5@helpline.com', '9876543249');

-- Doctor–Patient Assignments
INSERT INTO DoctorPatientAssignment VALUES
(1, 1),
(2, 2),
(4, 4),
(2, 5),
(1, 3);

-- SMS Notifications
INSERT INTO SMSNotification (recipient_phone, message, created_at) VALUES
('9876543210', 'Your case has been registered.', '2025-08-16 07:01:00'),
('9876543211', 'Doctor assigned to your case.', '2025-08-16 07:06:00'),
('9876543212', 'Please complete your medication.', '2025-08-16 07:11:00'),
('9876543213', 'Emergency alert sent to hospital.', '2025-08-16 07:16:00'),
('9876543214', 'Feedback request: Press 1 for Yes.', '2025-08-16 07:21:00');

-- Feedback
INSERT INTO Feedback (patient_id, rating, created_at) VALUES
(1, 5, '2025-08-16 07:30:00'),
(2, 4, '2025-08-16 07:35:00'),
(3, 3, '2025-08-16 07:40:00'),
(4, 5, '2025-08-16 07:45:00'),
(5, 2, '2025-08-16 07:50:00');

-- Prescription
INSERT INTO Prescription (patient_id, summary) VALUES
(1, 'Take paracetamol twice daily for 5 days.'),
(2, 'Use inhaler every morning and night.'),
(3, 'Apply skin ointment twice daily.'),
(4, 'Take aspirin and monitor BP daily.'),
(5, 'Use joint pain gel and avoid stairs.');

-- AuditLog
INSERT INTO AuditLog (patient_id, old_level, new_level, created_at, reason) VALUES
(1, 'Red', 'Blue', '2025-08-16 08:00:00', 'Manual downgrade after reassessment'),
(2, 'Yellow', 'Blue', '2025-08-16 08:05:00', 'AI misclassification suspected'),
(4, 'Red', 'Yellow', '2025-08-16 08:10:00', 'Doctor override'),
(5, 'Yellow', 'Blue', '2025-08-16 08:15:00', 'Patient condition improved'),
(3, 'Blue', 'Blue', '2025-08-16 08:20:00', 'No change');

-- Insert sample data into ASHA_Assignments
INSERT INTO ASHA_Assignments (asha_id, patient_id) VALUES
(1, 1),
(2, 2);

-- Insert sample data into HospitalResponse
INSERT INTO HospitalResponse (staff_id, patient_id) VALUES
(1, 1),
(2, 3);

-- Insert sample data into AdminManagement
INSERT INTO AdminManagement (admin_id, entity_type, entity_id) VALUES
(1, 'Doctor', 1),
(2, 'ASHAWorker', 2);
-- Insert sample data into CallAssistance
INSERT INTO CallAssistance (operator_id, user_id) VALUES
(1, 1),
(2, 2),
(3, 3);
