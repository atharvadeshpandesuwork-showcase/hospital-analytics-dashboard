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


def generate_beds(filepath, num_beds=25, seed=42):
    if seed:
        random.seed(seed)

    target_dir = os.path.dirname(os.path.abspath(filepath))
    _, admitted_patients = get_available_patient_data(target_dir)

    room_allocations = [
        ("R001", 4), ("R002", 1), ("R003", 1),
        ("R004", 4), ("R005", 1), ("R006", 1),
        ("R007", 4), ("R008", 1), ("R009", 1),
        ("R010", 4), ("R011", 1), ("R012", 1),
        ("R013", 1),
    ]

    patient_idx = 0
    current_date = datetime(2023, 5, 15)
    records = []
    bed_counter = 1

    # Typical occupied beds for realistic ward distribution
    occupied_bed_slots = [3, 5, 9, 11, 15, 17, 20, 23]

    for room_id, count in room_allocations:
        for _ in range(count):
            if bed_counter > num_beds:
                break
            bed_id = f"B{bed_counter:03d}"

            # Only assign beds to dynamically confirmed admitted patients
            if patient_idx < len(admitted_patients) and bed_counter in occupied_bed_slots:
                status = "Occupied"
                p_val = admitted_patients[patient_idx]
                patient_idx += 1
                admit_dt = current_date + timedelta(days=patient_idx * 12)
                from_val = format_mixed_date(admit_dt)
                till_val = None
            else:
                status, p_val, from_val, till_val = "Available", None, None, None

            records.append({
                "bed_id": mess_string(bed_id),
                "room_id": mess_string(room_id),
                "status": mess_string(status),
                "patient_id": mess_string(p_val) if p_val else None,
                "occupied_from": from_val,
                "occupied_till": till_val,
            })
            bed_counter += 1

    df = pd.DataFrame(records).rename(columns={
        "bed_id": " BED_ID ",
        "room_id": "Room_id",
        "status": " STATUS",
        "patient_id": "Patient_Id ",
        "occupied_from": " Occupied_From ",
        "occupied_till": "occupied_till ",
    })
    os.makedirs(target_dir, exist_ok=True)
    df.to_excel(filepath, index=False)