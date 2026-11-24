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


def generate_patient_tests(filepath, seed=42):
    """
    Generates synthetic diagnostic lab & radiology orders dynamically bound
    to actual patients from the patient master table.
    """
    if seed:
        random.seed(seed)

    target_dir = os.path.dirname(os.path.abspath(filepath))
    patient_ids, _ = get_available_patient_data(target_dir)

    diagnostic_pool = [
        {"t_id": "TEST001", "d_id": "D001", "result": "Normal", "notes": "WBC within normal limits", "amt": 500, "pay": "Cash", "disc": 0.0},
        {"t_id": "TEST003", "d_id": "D001", "result": "Abnormal", "notes": "Cholesterol elevated", "amt": 800, "pay": "Cash", "disc": 0.0},
        {"t_id": "TEST007", "d_id": "D001", "result": "Abnormal", "notes": "Minor arrhythmia detected", "amt": 1500, "pay": "Cash", "disc": None},
        {"t_id": "TEST004", "d_id": "D007", "result": "Abnormal", "notes": "Elevated liver enzymes", "amt": 1000, "pay": "Insurance", "disc": None},
        {"t_id": "TEST013", "d_id": "D007", "result": "Normal", "notes": "No parasites detected", "amt": 500, "pay": "Insurance", "disc": None},
        {"t_id": "TEST019", "d_id": "D007", "result": "Abnormal", "notes": "Gastric ulcers detected", "amt": 3500, "pay": "Insurance", "disc": None},
        {"t_id": "TEST017", "d_id": "D003", "result": "Abnormal", "notes": "Low bone density", "amt": 2500, "pay": "Cash", "disc": 0.0},
        {"t_id": "TEST001", "d_id": "D002", "result": "Normal", "notes": "All parameters within range", "amt": 500, "pay": "Insurance", "disc": None},
        {"t_id": "TEST009", "d_id": "D002", "result": "Abnormal", "notes": "Brain lesion detected", "amt": 4500, "pay": "Cash", "disc": 0.0},
        {"t_id": "TEST016", "d_id": "D011", "result": "Abnormal", "notes": "Elevated PSA levels", "amt": 1500, "pay": "Credit Card", "disc": None},
        {"t_id": "TEST011", "d_id": "D011", "result": "Abnormal", "notes": "Enlarged prostate confirmed", "amt": 1800, "pay": "Credit Card", "disc": None},
        {"t_id": "TEST005", "d_id": "D013", "result": "Abnormal", "notes": "Reduced kidney function", "amt": 1000, "pay": "Cash", "disc": None},
        {"t_id": "TEST011", "d_id": "D013", "result": "Abnormal", "notes": "Kidney stones visualized", "amt": 1800, "pay": "Cash", "disc": None},
        {"t_id": "TEST001", "d_id": "D015", "result": "Abnormal", "notes": "Reduced RBC count", "amt": 500, "pay": "Cash", "disc": 0.0},
        {"t_id": "TEST009", "d_id": "D015", "result": "Abnormal", "notes": "Tumor detected in left lung", "amt": 4500, "pay": "Insurance", "disc": None},
        {"t_id": "TEST008", "d_id": "D014", "result": "Abnormal", "notes": "Pulmonary fibrosis evident", "amt": 800, "pay": "Cash", "disc": None},
        {"t_id": "TEST018", "d_id": "D014", "result": "Abnormal", "notes": "Reduced lung capacity", "amt": 1800, "pay": "Cash", "disc": 0.0},
    ]

    base_date = datetime(2023, 5, 15)
    records = []

    # Allocate 1-2 tests across the dynamic patient IDs
    pt_counter = 1
    for p_id in patient_ids:
        # Assign 1 to 2 diagnostic orders per patient
        num_orders = random.choice([1, 2])
        for _ in range(num_orders):
            t_info = random.choice(diagnostic_pool)
            t_dt = base_date + timedelta(days=(pt_counter * 4) % 150)
            r_dt = t_dt + timedelta(days=random.choice([0, 1]))

            records.append({
                "patient_test_id": mess_string(f"PT{pt_counter:03d}"),
                "patient_id": mess_string(p_id),
                "test_id": mess_string(t_info["t_id"]),
                "doctor_id": mess_string(t_info["d_id"]),
                "test_date": format_mixed_date(t_dt),
                "result_date": format_mixed_date(r_dt),
                "status": mess_string("Completed"),
                "result": mess_string(t_info["result"]),
                "notes": mess_string(t_info["notes"]),
                "amount": int(t_info["amt"]),
                "payment_method": mess_string(t_info["pay"]),
                "discount": t_info["disc"],
            })
            pt_counter += 1

    df = pd.DataFrame(records)

    header_map = {
        "patient_test_id": " Patient_Test_ID ",
        "patient_id": "Patient_Id",
        "test_id": " TEST_ID ",
        "doctor_id": "Doctor_Id ",
        "test_date": " Test_Date ",
        "result_date": "Result_Date",
        "status": " STATUS ",
        "result": "Result",
        "notes": " Clinical_Notes ",
        "amount": "AMOUNT",
        "payment_method": " Payment_Method ",
        "discount": "Discount",
    }
    df.rename(columns=header_map, inplace=True)

    os.makedirs(target_dir, exist_ok=True)
    df.to_excel(filepath, index=False)