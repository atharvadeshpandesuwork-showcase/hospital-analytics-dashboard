import os
import random
from datetime import datetime, timedelta
import pandas as pd
from generators.patient_sync import get_available_patient_data


def mess_string(val):
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
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%d-%b-%Y",
        "%Y/%m/%d",
        " %d/%m/%Y ",
    ]
    return dt_obj.strftime(random.choice(formats))


def generate_bills(filepath, seed=42):
    """
    Generates synthetic billing records strictly synchronized with real patients
    from the patient table, preserving mathematical integrity and messy text.
    """
    if seed:
        random.seed(seed)

    target_dir = os.path.dirname(os.path.abspath(filepath))
    patient_ids, admitted_ids = get_available_patient_data(target_dir)

    current_date = datetime(2023, 5, 15)
    records = []

    for idx, p_id in enumerate(patient_ids, 1):
        bill_id = f"BILL{idx:03d}"
        
        # If patient is admitted, they are Inpatient or Major_Surgical
        if p_id in admitted_ids:
            care_type = random.choice(["Major_Surgical", "Inpatient"])
        else:
            care_type = random.choices(
                ["Major_Surgical", "Inpatient", "Outpatient"],
                weights=[0.15, 0.35, 0.50]
            )[0]

        current_date += timedelta(days=random.randint(2, 4))
        admit_dt = current_date

        if care_type == "Major_Surgical":
            stay_days = random.randint(7, 12)
            disch_dt = admit_dt + timedelta(days=stay_days) if p_id not in admitted_ids else None
            room_charges = stay_days * 1000
            surgery_charges = random.choice([25000, 35000, 50000, 60000, 75000])
            medicine_charges = random.randint(150, 450)
            test_charges = random.choice([2500, 3300, 4500, 5000, 6500])
            doctor_fees = random.choice([800, 850, 900, 950, 1200])
            other_charges = random.choice([1500, 2000, 3000])
            discount = random.choice([0, 1000, 2000, 5000])
        elif care_type == "Inpatient":
            stay_days = random.randint(4, 7)
            disch_dt = admit_dt + timedelta(days=stay_days) if p_id not in admitted_ids else None
            room_charges = stay_days * 1000
            surgery_charges = 0
            medicine_charges = random.randint(100, 300)
            test_charges = random.choice([0, 1500, 2000, 2800])
            doctor_fees = random.choice([700, 750, 800, 850])
            other_charges = random.choice([500, 1000, 1500])
            discount = random.choice([0, 0, 100, 500])
        else:
            disch_dt = None
            room_charges = 0
            surgery_charges = 0
            medicine_charges = random.randint(50, 250)
            test_charges = random.choice([0, 0, 1000, 2500, 5000])
            doctor_fees = random.choice([600, 650, 700, 800, 850])
            other_charges = 0
            discount = 0

        total_amount = (
            room_charges
            + surgery_charges
            + medicine_charges
            + test_charges
            + doctor_fees
            + other_charges
        )
        paid_amount = total_amount - discount

        records.append({
            "bill_id": mess_string(bill_id),
            "patient_id": mess_string(p_id),
            "admission_date": format_mixed_date(admit_dt),
            "discharge_date": format_mixed_date(disch_dt) if disch_dt else None,
            "room_charges": int(room_charges),
            "surgery_charges": int(surgery_charges),
            "medicine_charges": int(medicine_charges),
            "test_charges": int(test_charges),
            "doctor_fees": int(doctor_fees),
            "other_charges": int(other_charges),
            "total_amount": int(total_amount),
            "discount": int(discount),
            "paid_amount": int(paid_amount),
            "payment_status": mess_string(random.choice(["Paid", "Paid", "Pending"])),
            "payment_method": mess_string(random.choice(["Cash", "Credit Card", "Insurance"])),
        })

    df = pd.DataFrame(records).rename(columns={
        "bill_id": " BILL_ID ",
        "patient_id": "Patient_Id",
        "admission_date": " Admission_Date ",
        "discharge_date": "Discharge_Date ",
        "room_charges": "ROOM_CHARGES",
        "surgery_charges": " Surgery_Charges ",
        "medicine_charges": "medicine_charges",
        "test_charges": "Test_Charges ",
        "doctor_fees": "DOCTOR_FEES",
        "other_charges": " Other_Charges ",
        "total_amount": "Total_Amount",
        "discount": " DISCOUNT ",
        "paid_amount": "Paid_Amount ",
        "payment_status": " Payment_Status ",
        "payment_method": "PAYMENT_METHOD",
    })
    os.makedirs(target_dir, exist_ok=True)
    df.to_excel(filepath, index=False)