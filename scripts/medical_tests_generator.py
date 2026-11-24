import os
import random
import pandas as pd


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


def generate_medical_tests(filepath, seed=42):
    """
    Generates synthetic medical test records strictly preserving the exact 7 columns
    from Medical Tests.xlsx, with logical clinical mapping and messy text formatting.
    """
    if seed:
        random.seed(seed)

    tests_data = [
        {"id": "TEST001", "name": "Complete Blood Count", "cat": "Hematology", "dept": "DEPT015", "cost": 500, "duration": 30, "fasting": "Yes"},
        {"id": "TEST002", "name": "Blood Glucose", "cat": "Biochemistry", "dept": "DEPT012", "cost": 300, "duration": 15, "fasting": "Yes"},
        {"id": "TEST003", "name": "Lipid Profile", "cat": "Biochemistry", "dept": "DEPT012", "cost": 800, "duration": 30, "fasting": "Yes"},
        {"id": "TEST004", "name": "Liver Function Test", "cat": "Biochemistry", "dept": "DEPT007", "cost": 1000, "duration": 45, "fasting": "Yes"},
        {"id": "TEST005", "name": "Kidney Function Test", "cat": "Biochemistry", "dept": "DEPT013", "cost": 1000, "duration": 45, "fasting": "Yes"},
        {"id": "TEST006", "name": "Thyroid Profile", "cat": "Endocrinology", "dept": "DEPT012", "cost": 1200, "duration": 30, "fasting": "Yes"},
        {"id": "TEST007", "name": "Electrocardiogram (ECG)", "cat": "Cardiology", "dept": "DEPT001", "cost": 1500, "duration": 20, "fasting": "No"},
        {"id": "TEST008", "name": "X-Ray Chest", "cat": "Radiology", "dept": "DEPT014", "cost": 800, "duration": 15, "fasting": "No"},
        {"id": "TEST009", "name": "CT Scan", "cat": "Radiology", "dept": "DEPT014", "cost": 4500, "duration": 45, "fasting": "No"},
        {"id": "TEST010", "name": "MRI Scan", "cat": "Radiology", "dept": "DEPT014", "cost": 7500, "duration": 60, "fasting": "No"},
        {"id": "TEST011", "name": "Ultrasound", "cat": "Radiology", "dept": "DEPT014", "cost": 1800, "duration": 30, "fasting": "Depends"},
        {"id": "TEST012", "name": "Urine Analysis", "cat": "Pathology", "dept": "DEPT013", "cost": 400, "duration": 60, "fasting": "No"},
        {"id": "TEST013", "name": "Stool Analysis", "cat": "Pathology", "dept": "DEPT007", "cost": 500, "duration": 60, "fasting": "No"},
        {"id": "TEST014", "name": "Pap Smear", "cat": "Gynecology", "dept": "DEPT004", "cost": 1200, "duration": 30, "fasting": "No"},
        {"id": "TEST015", "name": "Mammogram", "cat": "Radiology", "dept": "DEPT004", "cost": 2000, "duration": 30, "fasting": "No"},
    ]

    records = []
    for t in tests_data:
        records.append({
            "test_id": mess_string(t["id"]),
            "test_name": mess_string(t["name"]),
            "category": mess_string(t["cat"]),
            "department_id": mess_string(t["dept"]),
            "cost": int(t["cost"]),                    # Intact numeric
            "duration_minutes": int(t["duration"]),    # Intact numeric
            "fasting_required": mess_string(t["fasting"]),
        })

    df = pd.DataFrame(records)

    # Inconsistent header names preserving the exact 7 columns
    header_map = {
        "test_id": " TEST_ID ",
        "test_name": "Test_Name",
        "category": " CATEGORY",
        "department_id": "Department_Id ",
        "cost": " COST ",
        "duration_minutes": "Duration_Minutes",
        "fasting_required": " Fasting_Required ",
    }
    df.rename(columns=header_map, inplace=True)

    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    df.to_excel(filepath, index=False)