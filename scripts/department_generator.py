import os
import random
import pandas as pd


def mess_string(val):
    if pd.isna(val) or val is None or val == "":
        return val
    s = str(val)
    choice = random.choice(
        [
            "lower",
            "upper",
            "mixed",
            "leading_space",
            "trailing_space",
            "both_spaces",
            "normal",
        ]
    )
    if choice == "lower":
        return s.lower()
    if choice == "upper":
        return s.upper()
    if choice == "mixed":
        return "".join(
            ch.lower() if idx % 2 == 0 else ch.upper()
            for idx, ch in enumerate(s)
        )
    if choice == "leading_space":
        return f"   {s}"
    if choice == "trailing_space":
        return f"{s}   "
    if choice == "both_spaces":
        return f"  {s}  "
    return s


def generate_departments(filepath, seed=42):
    if seed:
        random.seed(seed)

    depts = [
        ("DEPT001", "Cardiology", 3, "D001", 15, 1001),
        ("DEPT002", "Neurology", 4, "D002", 12, 1002),
        ("DEPT003", "Orthopedics", 2, "D003", 18, 1003),
        ("DEPT004", "Gynecology", 5, "D004", 14, 1004),
        ("DEPT005", "Pediatrics", 1, "D005", 16, 1005),
        ("DEPT006", "Dermatology", 3, "D006", 8, 1006),
        ("DEPT007", "Gastroenterology", 4, "D007", 10, 1007),
        ("DEPT008", "Ophthalmology", 2, "D008", 9, 1008),
        ("DEPT009", "ENT", 5, "D009", 7, 1009),
        ("DEPT010", "Psychiatry", 6, "D010", 6, 1010),
        ("DEPT011", "Urology", 3, "D011", 8, 1011),
        ("DEPT012", "Endocrinology", 4, "D012", 6, 1012),
        ("DEPT013", "Nephrology", 2, "D013", 9, 1013),
        ("DEPT014", "Pulmonology", 5, "D014", 10, 1014),
        ("DEPT015", "Oncology", 6, "D015", 14, 1015),
    ]

    records = []
    for d_id, name, floor, doc, staff, ext in depts:
        records.append(
            {
                "department_id": mess_string(d_id),
                "name": mess_string(name),
                "floor": int(floor),
                "head_doctor_id": mess_string(doc),
                "total_staff": int(staff),
                "phone_extension": int(ext),
            }
        )

    df = pd.DataFrame(records).rename(
        columns={
            "department_id": " DEPARTMENT_ID ",
            "name": "Dept_Name",
            "floor": " FLOOR ",
            "head_doctor_id": "Head_Doctor_Id",
            "total_staff": "total_staff ",
            "phone_extension": " Phone_Extension",
        }
    )
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    df.to_excel(filepath, index=False)