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


def generate_surgeries(filepath, seed=42):
    """
    Generates synthetic surgical consultation/appointment records dynamically
    assigned to every patient in the patient master, keeping the real-world column shift intact.
    """
    if seed:
        random.seed(seed)

    target_dir = os.path.dirname(os.path.abspath(filepath))
    patient_ids, _ = get_available_patient_data(target_dir)

    surgical_cases = [
        {"d_id": "D001", "time": "10:00:00", "status": "Completed", "reason": "Chest Pain", "notes": "Patient complained of chest pain", "sugg": "prescribed medication", "fee": 800, "pay": "Cash", "disc": 0},
        {"d_id": "D004", "time": "11:30:00", "status": "Completed", "reason": "Regular Checkup", "notes": "Regular gynecological checkup", "sugg": "all normal", "fee": 700, "pay": "Credit Card", "disc": 0},
        {"d_id": "D007", "time": "14:00:00", "status": "Completed", "reason": "Stomach Pain", "notes": "Patient has chronic gastritis", "sugg": "advised diet change", "fee": 850, "pay": "Insurance", "disc": 0},
        {"d_id": "D006", "time": "09:30:00", "status": "Completed", "reason": "Skin Rash", "notes": "Allergic reaction", "sugg": "prescribed antihistamines", "fee": 650, "pay": "Cash", "disc": 50},
        {"d_id": "D003", "time": "13:00:00", "status": "Completed", "reason": "Back Pain", "notes": "Lumbar strain", "sugg": "physiotherapy recommended", "fee": 800, "pay": "Insurance", "disc": 0},
        {"d_id": "D009", "time": "16:30:00", "status": "Completed", "reason": "Ear Infection", "notes": "Ear infection diagnosed", "sugg": "prescribed antibiotics", "fee": 700, "pay": "Credit Card", "disc": 0},
        {"d_id": "D002", "time": "10:00:00", "status": "Completed", "reason": "Severe Headache", "notes": "Possible migraine", "sugg": "further tests needed", "fee": 850, "pay": "Insurance", "disc": 0},
        {"d_id": "D010", "time": "11:30:00", "status": "Completed", "reason": "Anxiety Issues", "notes": "Patient suffering from anxiety", "sugg": "therapy recommended", "fee": 900, "pay": "Cash", "disc": 100},
        {"d_id": "D011", "time": "14:00:00", "status": "Completed", "reason": "Urinary Issues", "notes": "UTI diagnosed", "sugg": "prescribed antibiotics", "fee": 750, "pay": "Credit Card", "disc": 0},
        {"d_id": "D005", "time": "09:30:00", "status": "Completed", "reason": "Child Fever", "notes": "Child has viral fever", "sugg": "prescribed medication", "fee": 600, "pay": "Insurance", "disc": 0},
        {"d_id": "D013", "time": "13:00:00", "status": "Completed", "reason": "Kidney Pain", "notes": "Kidney stones suspected", "sugg": "tests ordered", "fee": 900, "pay": "Cash", "disc": 0},
        {"d_id": "D006", "time": "16:30:00", "status": "Completed", "reason": "Acne Treatment", "notes": "Severe acne", "sugg": "prescribed medication", "fee": 650, "pay": "Credit Card", "disc": 50},
        {"d_id": "D015", "time": "10:00:00", "status": "Completed", "reason": "Cancer Screening", "notes": "Routine cancer screening", "sugg": "tests ordered", "fee": 1200, "pay": "Insurance", "disc": 200},
        {"d_id": "D008", "time": "11:30:00", "status": "Completed", "reason": "Vision Problem", "notes": "Vision deterioration", "sugg": "new glasses prescribed", "fee": 700, "pay": "Cash", "disc": 0},
        {"d_id": "D001", "time": "14:00:00", "status": "Completed", "reason": "Heart Palpitations", "notes": "Heart arrhythmia suspected", "sugg": "ECG performed", "fee": 850, "pay": "Insurance", "disc": 0},
        {"d_id": "D012", "time": "09:30:00", "status": "Completed", "reason": "Diabetes Check", "notes": "Routine diabetes checkup", "sugg": "medication adjusted", "fee": 800, "pay": "Credit Card", "disc": 0},
        {"d_id": "D014", "time": "13:00:00", "status": "Completed", "reason": "Breathing Difficulty", "notes": "COPD exacerbation", "sugg": "treatment intensified", "fee": 900, "pay": "Cash", "disc": 100},
        {"d_id": "D004", "time": "16:30:00", "status": "Completed", "reason": "Pregnancy Confirmation", "notes": "Pregnancy confirmed", "sugg": "scheduled followup", "fee": 700, "pay": "Insurance", "disc": 0},
        {"d_id": "D007", "time": "10:00:00", "status": "Completed", "reason": "Liver Function", "notes": "Abnormal liver function", "sugg": "diet change advised", "fee": 850, "pay": "Credit Card", "disc": 0},
        {"d_id": "D003", "time": "11:30:00", "status": "Completed", "reason": "Joint Pain", "notes": "Arthritis diagnosed", "sugg": "medication prescribed", "fee": 800, "pay": "Cash", "disc": 0},
    ]

    base_date = datetime(2023, 5, 14)
    records = []

    for idx, p_id in enumerate(patient_ids, 1):
        item = surgical_cases[(idx - 1) % len(surgical_cases)]
        dt_val = base_date + timedelta(days=(idx * 5) % 155)

        # Shifted layout preserved
        records.append({
            "appointment_id": mess_string(f"APP{idx:03d}"),
            "patient_id": mess_string(p_id),
            "doctor_id": mess_string(item["d_id"]),
            "appointment_date": format_mixed_date(dt_val),
            "appointment_time": item["time"],
            "status": mess_string(item["status"]),
            "reason": mess_string(item["reason"]),
            "notes": mess_string(item["notes"]),
            "fees": mess_string(item["sugg"]),              # Shifted recommendation text
            "payment_method": int(item["fee"]),             # Shifted numeric fee
            "discount": mess_string(item["pay"]),           # Shifted payment method
            "Unnamed: 11": int(item["disc"]),               # Shifted numeric discount
        })

    df = pd.DataFrame(records)

    header_map = {
        "appointment_id": " APPOINTMENT_ID ",
        "patient_id": "Patient_Id",
        "doctor_id": "Doctor_Id ",
        "appointment_date": " Appointment_Date ",
        "appointment_time": "appointment_time",
        "status": " STATUS ",
        "reason": " Reason ",
        "notes": "Clinical_Notes",
        "fees": "fees",
        "payment_method": "payment_method",
        "discount": " discount ",
        "Unnamed: 11": "Unnamed: 11",
    }
    df.rename(columns=header_map, inplace=True)

    os.makedirs(target_dir, exist_ok=True)
    df.to_excel(filepath, index=False)