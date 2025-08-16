CREATE VIEW UserHealthSummary AS
SELECT 
    P.patient_id,
    P.name_patient,
    P.age,
    P.gender,
    P.location,
    P.urgency_level,
    P.medical_history,
    PR.summary AS prescription_summary,
    F.rating AS feedback_rating,
    A.old_level AS previous_urgency,
    A.new_level AS updated_urgency,
    A.created_at AS urgency_change_time
FROM Patient P
LEFT JOIN Prescription PR ON P.patient_id = PR.patient_id
LEFT JOIN Feedback F ON P.patient_id = F.patient_id
LEFT JOIN AuditLog A ON P.patient_id = A.patient_id;
