import os
import random
from datetime import datetime, timedelta
import pandas as pd
from generators.patient_sync import get_available_patient_data


def mess_string(val):
    """Injects erratic casing and padding spaces into strings."""
    if pd.isna(val) or val is None or val == "":
        return val
    s = str(val)
    choice = random.choice([
        "lower", "upper", "mixed", 
        "leading_space", "trailing_space", "both_spaces", "normal"
    ])
    if choice == "lower":
        return s.lower()
    if choice == "upper":
        return s.upper()
    if choice == "mixed":
        return "".join(ch.lower() if idx % 2 == 0 else ch.upper() for idx, ch in enumerate(s))
    if choice == "leading_space":
        return f"   {s}"
    if choice == "trailing_space":
        return f"{s}   "
    if choice == "both_spaces":
        return f"  {s}  "
    return s


def format_mixed_date(dt_obj):
    """Formats datetime objects into mixed real-world date strings."""
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%d-%b-%Y",
        "%Y/%m/%d",
        " %d/%m/%Y ",
    ]
    return dt_obj.strftime(random.choice(formats))


def generate_satisfaction_scores(filepath, seed=42):
    """
    Generates synthetic patient satisfaction reviews dynamically bound to
    existing patients from the patient master table.
    """
    if seed:
        random.seed(seed)

    target_dir = os.path.dirname(os.path.abspath(filepath))
    patient_ids, _ = get_available_patient_data(target_dir)

    feedback_templates = [
        {"d_id": "D001", "rate": 4, "fb": "The doctor was very attentive and explained everything well.", "dept": "Cardiology"},
        {"d_id": "D004", "rate": 5, "fb": "Excellent care and treatment. Very satisfied.", "dept": "Gynecology"},
        {"d_id": "D007", "rate": 3, "fb": "Treatment was good but had to wait too long.", "dept": "Gastroenterology"},
        {"d_id": "D006", "rate": 4, "fb": "Good diagnosis and treatment for my skin condition.", "dept": "Dermatology"},
        {"d_id": "D003", "rate": 5, "fb": "Very professional and the surgery was successful.", "dept": "Orthopedics"},
        {"d_id": "D009", "rate": 4, "fb": "Quick diagnosis and effective medication.", "dept": "ENT"},
        {"d_id": "D010", "rate": 5, "fb": "The doctor really understood my mental health concerns.", "dept": "Psychiatry"},
        {"d_id": "D011", "rate": 4, "fb": "Professional care and successful surgery.", "dept": "Urology"},
        {"d_id": "D013", "rate": 3, "fb": "Good treatment but communication could be better.", "dept": "Nephrology"},
        {"d_id": "D006", "rate": 5, "fb": "The skin treatment was very effective.", "dept": "Dermatology"},
        {"d_id": "D008", "rate": 4, "fb": "Vision has improved after treatment.", "dept": "Ophthalmology"},
        {"d_id": "D001", "rate": 5, "fb": "Excellent cardiac care and successful procedure.", "dept": "Cardiology"},
        {"d_id": "D012", "rate": 4, "fb": "Diabetes management advice was helpful.", "dept": "Endocrinology"},
        {"d_id": "D004", "rate": 5, "fb": "Very satisfied with the prenatal care.", "dept": "Gynecology"},
        {"d_id": "D007", "rate": 3, "fb": "Treatment was okay but needed more explanation.", "dept": "Gastroenterology"},
        {"d_id": "D002", "rate": 4, "fb": "Good care after my stroke.", "dept": "Neurology"},
        {"d_id": "D005", "rate": 5, "fb": "Excellent pediatric care for my child.", "dept": "Pediatrics"},
        {"d_id": "D009", "rate": 4, "fb": "My hearing has improved after treatment.", "dept": "ENT"},
        {"d_id": "D011", "rate": 3, "fb": "Surgery went well but recovery information was lacking.", "dept": "Urology"},
    ]

    base_date = datetime(2023, 5, 20)
    records = []

    # Map across actual patients present in patient master
    review_count = min(len(feedback_templates), len(patient_ids))
    for idx in range(review_count):
        p_id = patient_ids[idx % len(patient_ids)]
        tmpl = feedback_templates[idx]
        dt_val = base_date + timedelta(days=idx * 7)

        records.append({
            "satisfaction_id": mess_string(f"SAT{idx + 1:03d}"),
            "patient_id": mess_string(p_id),
            "doctor_id": mess_string(tmpl["d_id"]),
            "rating": int(tmpl["rate"]),
            "feedback": mess_string(tmpl["fb"]),
            "date": format_mixed_date(dt_val),
            "department": mess_string(tmpl["dept"]),
        })

    df = pd.DataFrame(records)

    header_map = {
        "satisfaction_id": " SATISFACTION_ID ",
        "patient_id": "Patient_Id",
        "doctor_id": " DOCTOR_ID ",
        "rating": " RATING ",
        "feedback": "Feedback",
        "date": " Survey_Date ",
        "department": " Department ",
    }
    df.rename(columns=header_map, inplace=True)

    os.makedirs(target_dir, exist_ok=True)
    df.to_excel(filepath, index=False)