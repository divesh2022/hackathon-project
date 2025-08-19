-- VisitLog
INSERT INTO VisitLog (asha_id, patient_id, visit_date, notes, offline_mode) VALUES
(1, 1, '2025-08-16 09:00:00', 'Checked vitals, advised rest.', 1),
(2, 2, '2025-08-16 09:30:00', 'Provided inhaler guidance.', 1),
(3, 3, '2025-08-16 10:00:00', 'Skin rash observed, referred to doctor.', 1),
(4, 4, '2025-08-16 10:30:00', 'BP high, escalated to hospital.', 1),
(5, 5, '2025-08-16 11:00:00', 'Joint pain severe, advised gel.', 1);

-- MedicationReminder
INSERT INTO MedicationReminder (patient_id, message, scheduled_time, status) VALUES
(1, 'Take paracetamol at 8 AM', '2025-08-17 08:00:00', 'pending'),
(2, 'Use inhaler at 9 AM', '2025-08-17 09:00:00', 'pending'),
(3, 'Apply ointment at 10 AM', '2025-08-17 10:00:00', 'pending'),
(4, 'Monitor BP at 7 AM', '2025-08-17 07:00:00', 'pending'),
(5, 'Apply gel at 6 PM', '2025-08-17 18:00:00', 'pending');

-- VoiceTipLibrary
INSERT INTO VoiceTipLibrary (language, topic, audio_file_path, last_used) VALUES
('Hindi', 'Handwashing', '/audio/hindi_handwash.mp3', '2025-08-15 08:00:00'),
('English', 'Mask Usage', '/audio/eng_mask.mp3', '2025-08-15 09:00:00'),
('Hindi', 'Clean Water', '/audio/hindi_water.mp3', '2025-08-15 10:00:00'),
('English', 'Social Distancing', '/audio/eng_distance.mp3', '2025-08-15 11:00:00'),
('Hindi', 'Mosquito Prevention', '/audio/hindi_mosquito.mp3', '2025-08-15 12:00:00');

-- DiseaseAlert
INSERT INTO DiseaseAlert (region, disease_name, message, created_at) VALUES
('Sundar Nagar', 'Dengue', 'Dengue outbreak alert. Use mosquito nets.', '2025-08-16 08:00:00'),
('Mandi', 'Flu', 'Seasonal flu rising. Wear masks.', '2025-08-16 08:05:00'),
('Kullu', 'Skin Infection', 'Avoid contaminated water.', '2025-08-16 08:10:00'),
('Bilaspur', 'COVID-19', 'Vaccination drive ongoing.', '2025-08-16 08:15:00'),
('Hamirpur', 'Chikungunya', 'Report joint pain symptoms.', '2025-08-16 08:20:00');

-- SymptomAnalysisLog
INSERT INTO SymptomAnalysisLog (user_id, symptoms, assigned_level, model_version, timestamp) VALUES
(1, 'Fever, cough', 'Yellow', 'v1.2.3', '2025-08-16 07:01:00'),
(2, 'Chest pain', 'Red', 'v1.2.3', '2025-08-16 07:06:00'),
(3, 'Skin rash', 'Blue', 'v1.2.3', '2025-08-16 07:11:00'),
(4, 'Headache', 'Blue', 'v1.2.3', '2025-08-16 07:16:00'),
(5, 'Shortness of breath', 'Yellow', 'v1.2.3', '2025-08-16 07:21:00');

-- ImageDiagnosis
INSERT INTO ImageDiagnosis (patient_id, image_path, diagnosis, confidence_score, timestamp) VALUES
(1, '/images/rash1.jpg', 'Fungal Infection', 0.87, '2025-08-16 09:00:00'),
(2, '/images/chest1.jpg', 'No visible anomaly', 0.92, '2025-08-16 09:05:00'),
(3, '/images/skin2.jpg', 'Eczema', 0.78, '2025-08-16 09:10:00'),
(4, '/images/eye1.jpg', 'Conjunctivitis', 0.81, '2025-08-16 09:15:00'),
(5, '/images/joint1.jpg', 'Arthritis signs', 0.85, '2025-08-16 09:20:00');

-- PrescriptionSummary
INSERT INTO PrescriptionSummary (prescription_id, dosage, instructions, side_effects) VALUES
(1, '500mg twice daily', 'Take after meals', 'May cause drowsiness'),
(2, '2 puffs morning & night', 'Shake well before use', 'Dry mouth'),
(3, 'Apply thin layer', 'Do not expose to sunlight', 'Skin irritation'),
(4, '75mg daily', 'Monitor BP regularly', 'Stomach upset'),
(5, 'Apply gel twice', 'Avoid stairs', 'Mild burning sensation');

-- LanguagePreference
INSERT INTO LanguagePreference (user_id, preferred_language, region, accent_notes) VALUES
(1, 'Hindi', 'Sundar Nagar', 'Local Himachali accent'),
(2, 'Hindi', 'Mandi', 'Clear diction'),
(3, 'English', 'Kullu', 'Neutral accent'),
(4, 'Hindi', 'Bilaspur', 'Soft tone'),
(5, 'Hindi', 'Hamirpur', 'Fast speech pattern');

-- AIResponseLog
INSERT INTO AIResponseLog (timestamp, phone_no, urgency_level, location, name_of_caller, name_of_patient, problem_reported, advice_given) VALUES
('2025-08-16 07:01:00', '9876543215', 'Yellow', 'Sundar Nagar', 'Caller1', 'Ravi Kumar', 'Fever, cough', 'Visit ASHA worker within 24 hours'),
('2025-08-16 07:06:00', '9876543216', 'Red', 'Mandi', 'Caller2', 'Meena Devi', 'Chest pain', 'Ambulance dispatched'),
('2025-08-16 07:11:00', '9876543217', 'Blue', 'Kullu', 'Caller3', 'Amit Thakur', 'Skin rash', 'Apply ointment and monitor'),
('2025-08-16 07:16:00', '9876543218', 'Blue', 'Bilaspur', 'Caller4', 'Sunita Sharma', 'Headache', 'Rest and hydration advised'),
('2025-08-16 07:21:00', '9876543219', 'Yellow', 'Hamirpur', 'Caller5', 'Rajesh Rana', 'Shortness of breath', 'Doctor consultation scheduled');
