import os
import random
from datetime import datetime
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


def generate_staff(filepath, seed=42):
    """
    Generates synthetic nursing and ward support staff records preserving the exact 12 columns
    from Staff.xlsx, including the unquoted split address columns and messy text formatting.
    """
    if seed:
        random.seed(seed)

    staff_base = [
        {"id": "S001", "name": "Anand Kumar", "dept": "DEPT001", "role": "Nurse", "sal": 45000, "join": "2018-01-10", "shift": "Morning", "phone": 9876543210, "email": "anand.kumar@hospital.com", "addr": 123, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S002", "name": "Sunita Verma", "dept": "DEPT001", "role": "Nurse", "sal": 42000, "join": "2019-03-15", "shift": "Evening", "phone": 8765432109, "email": "sunita.verma@hospital.com", "addr": 124, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S003", "name": "Rajiv Singh", "dept": "DEPT001", "role": "Ward Boy", "sal": 25000, "join": "2020-06-20", "shift": "Night", "phone": 7654321098, "email": "rajiv.singh@hospital.com", "addr": 125, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S004", "name": "Meena Patel", "dept": "DEPT002", "role": "Nurse", "sal": 44000, "join": "2018-05-12", "shift": "Morning", "phone": 6543210987, "email": "meena.patel@hospital.com", "addr": 126, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S005", "name": "Suresh Nair", "dept": "DEPT002", "role": "Nurse", "sal": 43000, "join": "2019-07-18", "shift": "Evening", "phone": 5432109876, "email": "suresh.nair@hospital.com", "addr": 127, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S006", "name": "Kavita Menon", "dept": "DEPT002", "role": "Ward Boy", "sal": 26000, "join": "2020-09-25", "shift": "Night", "phone": 4321098765, "email": "kavita.menon@hospital.com", "addr": 128, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S007", "name": "Rahul Sharma", "dept": "DEPT003", "role": "Nurse", "sal": 46000, "join": "2017-08-15", "shift": "Morning", "phone": 3210987654, "email": "rahul.sharma@hospital.com", "addr": 129, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S008", "name": "Priya Singh", "dept": "DEPT003", "role": "Nurse", "sal": 44000, "join": "2018-10-20", "shift": "Evening", "phone": 2109876543, "email": "priya.singh@hospital.com", "addr": 130, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S009", "name": "Amit Kumar", "dept": "DEPT003", "role": "Ward Boy", "sal": 27000, "join": "2019-12-10", "shift": "Night", "phone": 1098765432, "email": "amit.kumar@hospital.com", "addr": 131, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S010", "name": "Neha Joshi", "dept": "DEPT004", "role": "Nurse", "sal": 45000, "join": "2018-02-05", "shift": "Morning", "phone": 9876543220, "email": "neha.joshi@hospital.com", "addr": 132, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S011", "name": "Vikram Malhotra", "dept": "DEPT004", "role": "Nurse", "sal": 43000, "join": "2019-04-15", "shift": "Evening", "phone": 8765432119, "email": "vikram.m@hospital.com", "addr": 133, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S012", "name": "Nisha Reddy", "dept": "DEPT004", "role": "Ward Boy", "sal": 26000, "join": "2020-07-25", "shift": "Night", "phone": 7654321108, "email": "nisha.r@hospital.com", "addr": 134, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S013", "name": "Deepak Gupta", "dept": "DEPT005", "role": "Nurse", "sal": 47000, "join": "2017-03-10", "shift": "Morning", "phone": 6543210997, "email": "deepak.g@hospital.com", "addr": 135, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S014", "name": "Anita Saxena", "dept": "DEPT005", "role": "Nurse", "sal": 45000, "join": "2018-05-20", "shift": "Evening", "phone": 5432109886, "email": "anita.s@hospital.com", "addr": 136, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S015", "name": "Sanjay Bhatia", "dept": "DEPT005", "role": "Ward Boy", "sal": 28000, "join": "2019-08-15", "shift": "Night", "phone": 4321098775, "email": "sanjay.b@hospital.com", "addr": 137, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S016", "name": "Divya Mehta", "dept": "DEPT006", "role": "Nurse", "sal": 44000, "join": "2018-06-25", "shift": "Morning", "phone": 3210987664, "email": "divya.m@hospital.com", "addr": 138, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S017", "name": "Rakesh Das", "dept": "DEPT007", "role": "Nurse", "sal": 45000, "join": "2018-09-10", "shift": "Morning", "phone": 2109876553, "email": "rakesh.d@hospital.com", "addr": 139, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S018", "name": "Anjali Khanna", "dept": "DEPT008", "role": "Nurse", "sal": 43000, "join": "2019-01-15", "shift": "Morning", "phone": 1098765442, "email": "anjali.k@hospital.com", "addr": 140, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S019", "name": "Vivek Iyer", "dept": "DEPT009", "role": "Nurse", "sal": 44000, "join": "2018-11-05", "shift": "Morning", "phone": 9876543230, "email": "vivek.i@hospital.com", "addr": 141, "u10": "Staff Quarters", "u11": "Hospital Campus"},
        {"id": "S020", "name": "Geeta Nair", "dept": "DEPT010", "role": "Nurse", "sal": 42000, "join": "2019-12-20", "shift": "Morning", "phone": 8765432129, "email": "geeta.n@hospital.com", "addr": 142, "u10": "Staff Quarters", "u11": "Hospital Campus"},
    ]

    records = []
    for s_item in staff_base:
        j_dt = datetime.strptime(s_item["join"], "%Y-%m-%d")

        records.append({
            "staff_id": mess_string(s_item["id"]),
            "name": mess_string(s_item["name"]),
            "department_id": mess_string(s_item["dept"]),
            "role": mess_string(s_item["role"]),
            "salary": int(s_item["sal"]),                          # Pure numeric
            "joining_date": format_mixed_date(j_dt),
            "shift": mess_string(s_item["shift"]),
            "phone": int(s_item["phone"]),                         # Pure numeric
            "email": mess_string(s_item["email"]),
            "address": int(s_item["addr"]),                        # House number
            "Unnamed: 10": mess_string(s_item["u10"]),             # Unquoted address component
            "Unnamed: 11": mess_string(s_item["u11"]),             # Unquoted address component
        })

    df = pd.DataFrame(records)

    # Inconsistent header names preserving the exact 12 columns
    header_map = {
        "staff_id": " STAFF_ID ",
        "name": "Staff_Name",
        "department_id": "Department_Id ",
        "role": " ROLE ",
        "salary": "SALARY",
        "joining_date": " Joining_Date ",
        "shift": "Shift",
        "phone": "Phone_Number",
        "email": " Email_Address ",
        "address": "address",
        "Unnamed: 10": "Unnamed: 10",
        "Unnamed: 11": "Unnamed: 11",
    }
    df.rename(columns=header_map, inplace=True)

    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    df.to_excel(filepath, index=False)