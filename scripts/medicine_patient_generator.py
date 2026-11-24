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


def generate_medicine_patient(filepath, num_rows=250, seed=42):
    """
    Generates synthetic prescription/dispense logs linking dynamic patients
    to medicines MED001-MED015 with realistic dates and messy text formatting.
    """
    if seed:
        random.seed(seed)

    target_dir = os.path.dirname(os.path.abspath(filepath))
    patient_ids, _ = get_available_patient_data(target_dir)

    medicine_pool = [f"MED{i:03d}" for i in range(1, 16)]
    base_start = datetime(2023, 5, 15)

    records = []
    for _ in range(num_rows):
        p_id = random.choice(patient_ids)
        m_id = random.choice(medicine_pool)
        qty_val = random.randint(3, 12)
        dispense_dt = base_start + timedelta(days=random.randint(0, 160))

        records.append({
            "patient_id": mess_string(p_id),
            "medicine_id": mess_string(m_id),
            "qty": int(qty_val),
            "date": format_mixed_date(dispense_dt),
        })

    df = pd.DataFrame(records)

    header_map = {
        "patient_id": " PATIENT_ID",
        "medicine_id": "medicine_id ",
        "qty": " Qty ",
        "date": "Dispensed_Date ",
    }
    df.rename(columns=header_map, inplace=True)

    os.makedirs(target_dir, exist_ok=True)
    df.to_excel(filepath, index=False)