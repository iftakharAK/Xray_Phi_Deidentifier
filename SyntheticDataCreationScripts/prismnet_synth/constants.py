from __future__ import annotations

PHI_CATEGORIES = [
    "patient_name",
    "patient_id",
    "dob",
    "exam_date",
    "exam_time",
    "hospital_name",
    "physician_name",
    "age_sex",
]

BUDGET_CATEGORY_MAP = {
    0.25: ["patient_name", "patient_id"],
    0.50: ["patient_name", "patient_id", "dob"],
    0.75: ["patient_name", "patient_id", "dob", "exam_date", "physician_name"],
    1.00: PHI_CATEGORIES[:],
}

POLICY_CATEGORY_MAP = {
    "hospital_A": ["patient_name", "patient_id", "dob"],
    "hospital_B": ["patient_name", "patient_id", "exam_date", "hospital_name"],
    "hospital_C": PHI_CATEGORIES[:],
}

HOSPITAL_PREFIXES = [
    "Mercy", "Saint Mary", "Saint Luke", "County", "Regional", "Metro",
    "Northside", "Southside", "Westlake", "Eastview", "Valley", "Central",
    "University", "Community", "Grand", "River", "Lake", "Pine", "Oak",
    "Summit", "Hope", "Providence", "Heritage", "Unity", "General",
    "Midwest", "Lakeside", "Greenview", "Hillcrest", "Brookside",
    "Silverline", "Royal", "National", "Premier", "Harbor", "Crescent",
]

HOSPITAL_MIDDLES = [
    "Medical", "Diagnostic", "Radiology", "Pulmonary", "Chest", "Imaging",
    "Clinical", "Health", "Emergency", "Specialty", "Memorial",
    "Cardio", "Oncology", "Trauma", "Care", "Thoracic",
]

HOSPITAL_SUFFIXES = [
    "Center", "Hospital", "Clinic", "Institute", "Facility",
    "Medical Center", "Diagnostic Center", "Imaging Center",
    "Research Center", "Chest Institute", "Health System",
]

DEPARTMENTS = [
    "Radiology", "Pulmonology", "Emergency", "ICU", "Internal Medicine",
    "Chest Clinic", "Imaging Center", "Thoracic Unit", "Outpatient Imaging",
    "Critical Care", "Respiratory Care",
]

NON_PHI_MARKERS = [
    "AP", "PA", "LAT", "PORTABLE", "UPRIGHT", "SUPINE",
    "CHEST", "L", "R", "LEFT", "RIGHT",
]
