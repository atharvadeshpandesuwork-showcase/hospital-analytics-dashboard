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


def generate_appointments(filepath, seed=42):
    """
    Dynamically maps every patient discovered in the patient master table
    to an appointment with a specialist doctor (D001 - D015).
    """
    if seed:
        random.seed(seed)

    target_dir = os.path.dirname(os.path.abspath(filepath))
    patient_ids, _ = get_available_patient_data(target_dir)

    doctor_pool = [
        {"d_id": "D001", "fee": 850, "cases": [("Chest Pain", "Patient complained of chest pain", "prescribed medication", "Heart attack"), ("Heart Palpitations", "Arrhythmia suspected", "ECG performed", "Arrhythmia")]},
        {"d_id": "D002", "fee": 900, "cases": [("Severe Headache", "Possible migraine", "further tests needed", "Migraine"), ("Stroke Symptoms", "TIA suspected", "hospitalization recommended", "Transient ischemic attack")]},
        {"d_id": "D003", "fee": 800, "cases": [("Back Pain", "Lumbar strain", "physiotherapy recommended", "Lumbar disc disorder"), ("Joint Pain", "Arthritis diagnosed", "medication prescribed", "Osteoarthritis")]},
        {"d_id": "D004", "fee": 700, "cases": [("Regular Checkup", "Regular gynecological checkup", "all normal", "Routine examination"), ("Pregnancy Confirmation", "Pregnancy confirmed", "scheduled followup", "Normal pregnancy")]},
        {"d_id": "D005", "fee": 600, "cases": [("Child Fever", "Child has viral fever", "prescribed medication", "Viral fever"), ("Child Vaccination", "Routine vaccination", "next appointment scheduled", "Routine immunization")]},
        {"d_id": "D006", "fee": 650, "cases": [("Skin Rash", "Allergic reaction", "prescribed antihistamines", "Contact dermatitis"), ("Acne Treatment", "Severe acne", "prescribed medication", "Acne vulgaris"), ("Eczema", "Eczema flare-up", "topical steroids prescribed", "Atopic dermatitis")]},
        {"d_id": "D007", "fee": 850, "cases": [("Stomach Pain", "Patient has chronic gastritis", "advised diet change", "Gastritis"), ("Liver Function", "Abnormal liver function", "diet change advised", "Hepatic dysfunction")]},
        {"d_id": "D008", "fee": 700, "cases": [("Vision Problem", "Vision deterioration", "new glasses prescribed", "Refractive error"), ("Cataract Examination", "Cataract diagnosed", "surgery recommended", "Cataract")]},
        {"d_id": "D009", "fee": 700, "cases": [("Ear Infection", "Ear infection diagnosed", "prescribed antibiotics", "Otitis media"), ("Hearing Loss", "Mild hearing loss", "hearing aid recommended", "Sensorineural hearing loss")]},
        {"d_id": "D010", "fee": 900, "cases": [("Anxiety Issues", "Patient suffering from anxiety", "therapy recommended", "Generalized anxiety"), ("Depression", "Clinical depression diagnosed", "therapy started", "Major depressive disorder")]},
        {"d_id": "D011", "fee": 800, "cases": [("Urinary Issues", "UTI diagnosed", "prescribed antibiotics", "Urinary tract infection"), ("Prostate Examination", "Enlarged prostate", "medication prescribed", "Benign prostatic hyperplasia")]},
        {"d_id": "D012", "fee": 800, "cases": [("Diabetes Check", "Routine diabetes checkup", "medication adjusted", "Diabetes mellitus")]},
        {"d_id": "D013", "fee": 900, "cases": [("Kidney Pain", "Kidney stones suspected", "tests ordered", "Nephrolithiasis"), ("Renal Checkup", "Renal function deteriorating", "admission advised", "Chronic kidney disease")]},
        {"d_id": "D014", "fee": 900, "cases": [("Breathing Difficulty", "COPD exacerbation", "treatment intensified", "COPD"), ("Pneumonia Symptoms", "Pneumonia confirmed", "hospitalization recommended", "Bacterial pneumonia")]},
        {"d_id": "D015", "fee": 1200, "cases": [("Cancer Screening", "Routine cancer screening", "tests ordered", "Oncology evaluation"), ("Cancer Followup", "Cancer in remission", "monitoring continued", "Oncology follow-up")]},
    ]

    base_date = datetime(2023, 5, 14)
    records = []

    for idx, p_id in enumerate(patient_ids, 1):
        doc = doctor_pool[(idx - 1) % len(doctor_pool)]
        reason, notes, sugg, diag = random.choice(doc["cases"])
        
        appt_date = base_date + timedelta(days=(idx * 5) % 155)
        appt_time = f"{random.randint(9, 16):02d}:{random.choice(['00', '15', '30', '45'])}:00"

        records.append({
            "appointment_id": mess_string(f"APP{idx:03d}"),
            "patient_id": mess_string(p_id),
            "doctor_id": mess_string(doc["d_id"]),
            "appointment_date": format_mixed_date(appt_date),
            "appointment_time": appt_time,
            "status": mess_string("Completed"),
            "reason": mess_string(reason),
            "notes": mess_string(notes),
            "suggest": mess_string(sugg),
            "fees": int(doc["fee"]),
            "payment_method": mess_string(random.choice(["Cash", "Credit Card", "Insurance"])),
            "discount": int(random.choice([0, 0, 50, 100, 200])),
            "diagnosis": mess_string(diag),
        })

    df = pd.DataFrame(records)

    header_map = {
        "appointment_id": "Appointment_Id ",
        "patient_id": " PATIENT_ID",
        "doctor_id": "Doctor_id",
        "appointment_date": " Appointment_Date ",
        "appointment_time": "appointment_time ",
        "status": "STATUS",
        "reason": " Reason",
        "notes": " NOTES ",
        "suggest": "Suggest",
        "fees": "FEES ",
        "payment_method": " Payment_Method",
        "discount": "Discount",
        "diagnosis": " DIAGNOSIS ",
    }
    df.rename(columns=header_map, inplace=True)

    os.makedirs(target_dir, exist_ok=True)
    df.to_excel(filepath, index=False)