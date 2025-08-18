-- 3. Admin: Full access to all tables
GRANT SELECT, INSERT, UPDATE, DELETE ON Patient TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON NaiveUser TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON Caregiver TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON CallCenterOperator TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON Doctor TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ASHAWorker TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON HospitalStaff TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON Admin TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON CallAssistance TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ASHA_Assignments TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON HospitalResponse TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON AdminManagement TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON DoctorPatientAssignment TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON SMSNotification TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON Prescription TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON AuditLog TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON Feedback TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON VisitLog TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON MedicationReminder TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON VoiceTipLibrary TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON DiseaseAlert TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON SymptomAnalysisLog TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ImageDiagnosis TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON PrescriptionSummary TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON LanguagePreference TO admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON AIResponseLog TO admin_user;

-- 4. Doctor
GRANT SELECT ON DoctorPatientAssignment TO doctor_user;
GRANT SELECT ON Patient TO doctor_user;
GRANT INSERT ON Prescription TO doctor_user;
GRANT UPDATE ON Doctor TO doctor_user;
GRANT SELECT ON AuditLog TO doctor_user;
GRANT SELECT ON Feedback TO doctor_user;

-- 5. ASHA Worker
GRANT SELECT ON ASHA_Assignments TO asha_user;
GRANT SELECT ON Patient TO asha_user;
GRANT INSERT ON VisitLog TO asha_user;
GRANT SELECT ON AuditLog TO asha_user;

-- 6. Patient
GRANT SELECT ON Patient TO patient_user;
GRANT INSERT ON Feedback TO patient_user;
GRANT SELECT ON SMSNotification TO patient_user;
GRANT SELECT ON Prescription TO patient_user;

-- 7. CallCenter Operator
GRANT INSERT ON CallAssistance TO operator_user;
GRANT SELECT ON NaiveUser TO operator_user;
GRANT INSERT ON SymptomAnalysisLog TO operator_user;
GRANT INSERT ON SMSNotification TO operator_user;

-- 8. Hospital Staff
GRANT SELECT ON HospitalResponse TO staff_user;
GRANT SELECT ON Patient TO staff_user;
GRANT INSERT ON HospitalResponse TO staff_user;
GRANT UPDATE ON HospitalStaff TO staff_user;

-- 9. Caregiver
GRANT SELECT ON Patient TO caregiver_user;
GRANT INSERT ON Feedback TO caregiver_user;
GRANT SELECT ON SMSNotification TO caregiver_user;

-- 10. Naive User
GRANT INSERT ON NaiveUser TO naive_user;
GRANT INSERT ON CallAssistance TO naive_user;
GRANT SELECT ON SMSNotification TO naive_user;
