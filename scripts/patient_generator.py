import os
import random
from datetime import datetime, timedelta
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


def generate_patients(filepath, seed=42):
    """
    Generates synthetic patient records strictly preserving the exact 14 columns
    from patient.xlsx, with logical admission/discharge tracking and messy text formatting.
    """
    if seed:
        random.seed(seed)

    patient_records = [
        {"id": "P001", "name": "Rahul Sharma", "age": 45, "gender": "Male", "weight": 78, "bg": "B+", "addr": "Park Street", "state": "Delhi", "phone": 9876543210, "email": "rahul.sharma@email.com", "admit": "2023-05-15", "disch": "2023-05-20", "status": "Discharged", "img": "https://i.ibb.co/4ZXXPz6S/P4.jpg"},
        {"id": "P002", "name": "Priya Singh", "age": 32, "gender": "Female", "weight": 65, "bg": "O+", "addr": "Lake Road", "state": "Mumbai", "phone": 8765432109, "email": "priya.singh@email.com", "admit": "2023-05-18", "disch": "2023-05-25", "status": "Discharged", "img": "https://i.ibb.co/DPS8djNk/p-m-5.jpg"},
        {"id": "P003", "name": "Amit Kumar", "age": 58, "gender": "Male", "weight": 82, "bg": "AB+", "addr": "Hill View", "state": "Bangalore", "phone": 7654321098, "email": "amit.kumar@email.com", "admit": "2023-05-20", "disch": "2023-05-30", "status": "Discharged", "img": "https://i.ibb.co/spTJqyKK/P3-1.jpg"},
        {"id": "P004", "name": "Sneha Patel", "age": 28, "gender": "Female", "weight": 59, "bg": "A-", "addr": "River Side", "state": "Chennai", "phone": 6543210987, "email": "sneha.patel@email.com", "admit": "2023-06-02", "disch": "2023-06-10", "status": "Discharged", "img": "https://i.ibb.co/S15ts9X/p-m3.jpg"},
        {"id": "P005", "name": "Vikram Malhotra", "age": 52, "gender": "Male", "weight": 88, "bg": "O-", "addr": "Mountain View", "state": "Kolkata", "phone": 5432109876, "email": "vikram.malhotra@email.com", "admit": "2023-06-05", "disch": "2023-06-15", "status": "Discharged", "img": "https://i.ibb.co/6RN9f482/P2.jpg"},
        {"id": "P006", "name": "Nisha Joshi", "age": 37, "gender": "Female", "weight": 62, "bg": "B-", "addr": "Valley Road", "state": "Hyderabad", "phone": 4321098765, "email": "nisha.joshi@email.com", "admit": "2023-06-10", "disch": "2023-06-14", "status": "Discharged", "img": "https://i.ibb.co/DPS8djNk/p-m-5.jpg"},
        {"id": "P007", "name": "Suresh Reddy", "age": 63, "gender": "Male", "weight": 75, "bg": "A+", "addr": "Cloud Street", "state": "Pune", "phone": 3210987654, "email": "suresh.reddy@email.com", "admit": "2023-06-15", "disch": None, "status": "Admitted", "img": "https://i.ibb.co/gL9c0QTx/P1-1.jpg"},
        {"id": "P008", "name": "Meera Gupta", "age": 41, "gender": "Female", "weight": 70, "bg": "AB-", "addr": "Star Avenue", "state": "Ahmedabad", "phone": 2109876543, "email": "meera.gupta@email.com", "admit": "2023-06-18", "disch": "2023-06-25", "status": "Discharged", "img": "https://i.ibb.co/S15ts9X/p-m3.jpg"},
        {"id": "P009", "name": "Rajiv Verma", "age": 49, "gender": "Male", "weight": 85, "bg": "B+", "addr": "Moon Road", "state": "Jaipur", "phone": 1098765432, "email": "rajiv.verma@email.com", "admit": "2023-06-20", "disch": "2023-06-30", "status": "Discharged", "img": "https://i.ibb.co/4ZXXPz6S/P4.jpg"},
        {"id": "P010", "name": "Kavita Rao", "age": 35, "gender": "Female", "weight": 61, "bg": "O+", "addr": "Sun Lane", "state": "Lucknow", "phone": 9876543220, "email": "kavita.rao@email.com", "admit": "2023-07-01", "disch": None, "status": "Admitted", "img": "https://i.ibb.co/DPS8djNk/p-m-5.jpg"},
        {"id": "P011", "name": "Deepak Menon", "age": 55, "gender": "Male", "weight": 79, "bg": "AB+", "addr": "Galaxy Avenue", "state": "Chandigarh", "phone": 8765432119, "email": "deepak.menon@email.com", "admit": "2023-07-05", "disch": "2023-07-12", "status": "Discharged", "img": "https://i.ibb.co/6RN9f482/P2.jpg"},
        {"id": "P012", "name": "Anita Saxena", "age": 30, "gender": "Female", "weight": 58, "bg": "A-", "addr": "Neptune Road", "state": "Bhopal", "phone": 7654321108, "email": "anita.saxena@email.com", "admit": "2023-07-10", "disch": "2023-07-15", "status": "Discharged", "img": "https://i.ibb.co/PGLMhWdT/p-m-4.png"},
        {"id": "P013", "name": "Sanjay Bhatia", "age": 60, "gender": "Male", "weight": 77, "bg": "O-", "addr": "Jupiter Street", "state": "Indore", "phone": 6543210997, "email": "sanjay.bhatia@email.com", "admit": "2023-07-15", "disch": None, "status": "Admitted", "img": "https://i.ibb.co/4ZXXPz6S/P4.jpg"},
        {"id": "P014", "name": "Pooja Mehta", "age": 34, "gender": "Female", "weight": 63, "bg": "B-", "addr": "Mars Lane", "state": "Nagpur", "phone": 5432109886, "email": "pooja.mehta@email.com", "admit": "2023-07-18", "disch": "2023-07-25", "status": "Discharged", "img": "https://i.ibb.co/S15ts9X/p-m3.jpg"},
        {"id": "P015", "name": "Ravi Khanna", "age": 50, "gender": "Male", "weight": 81, "bg": "A+", "addr": "Venus Road", "state": "Kanpur", "phone": 4321098775, "email": "ravi.khanna@email.com", "admit": "2023-07-20", "disch": "2023-07-28", "status": "Discharged", "img": "https://i.ibb.co/6RN9f482/P2.jpg"},
        {"id": "P016", "name": "Sonali Das", "age": 39, "gender": "Female", "weight": 66, "bg": "AB-", "addr": "Earth Avenue", "state": "Kochi", "phone": 3210987664, "email": "sonali.das@email.com", "admit": "2023-08-01", "disch": "2023-08-10", "status": "Discharged", "img": "https://i.ibb.co/PGLMhWdT/p-m-4.png"},
        {"id": "P017", "name": "Ajay Nair", "age": 61, "gender": "Male", "weight": 76, "bg": "B+", "addr": "Mercury Street", "state": "Guwahati", "phone": 2109876553, "email": "ajay.nair@email.com", "admit": "2023-08-05", "disch": None, "status": "Admitted", "img": "https://i.ibb.co/4ZXXPz6S/P4.jpg"},
        {"id": "P018", "name": "Neha Sharma", "age": 33, "gender": "Female", "weight": 60, "bg": "O+", "addr": "Saturn Road", "state": "Patna", "phone": 1098765442, "email": "neha.sharma@email.com", "admit": "2023-08-10", "disch": "2023-08-15", "status": "Discharged", "img": "https://i.ibb.co/PGLMhWdT/p-m-4.png"},
        {"id": "P019", "name": "Vinod Kapoor", "age": 57, "gender": "Male", "weight": 80, "bg": "AB+", "addr": "Pluto Avenue", "state": "Vadodara", "phone": 9876543230, "email": "vinod.kapoor@email.com", "admit": "2023-08-15", "disch": "2023-08-25", "status": "Discharged", "img": "https://i.ibb.co/6RN9f482/P2.jpg"},
        {"id": "P020", "name": "Anjali Mathur", "age": 36, "gender": "Female", "weight": 64, "bg": "A-", "addr": "Comet Lane", "state": "Vishakhapatnam", "phone": 8765432129, "email": "anjali.mathur@email.com", "admit": "2023-08-20", "disch": None, "status": "Admitted", "img": "https://i.ibb.co/PGLMhWdT/p-m-4.png"},
        {"id": "P021", "name": "Dinesh Agarwal", "age": 53, "gender": "Male", "weight": 83, "bg": "O-", "addr": "Meteor Road", "state": "Surat", "phone": 7654321118, "email": "dinesh.agarwal@email.com", "admit": "2023-09-01", "disch": "2023-09-10", "status": "Discharged", "img": "https://i.ibb.co/4ZXXPz6S/P4.jpg"},
        {"id": "P022", "name": "Sunita Verma", "age": 38, "gender": "Female", "weight": 65, "bg": "B-", "addr": "Galaxy Street", "state": "Ranchi", "phone": 6543210987, "email": "sunita.verma@email.com", "admit": "2023-09-05", "disch": "2023-09-12", "status": "Discharged", "img": "https://i.ibb.co/4Csnhg1/p-m2.jpg"},
        {"id": "P023", "name": "Kishore Kumar", "age": 64, "gender": "Male", "weight": 74, "bg": "A+", "addr": "Universe Lane", "state": "Trivandrum", "phone": 5432109876, "email": "kishore.kumar@email.com", "admit": "2023-09-10", "disch": None, "status": "Admitted", "img": "https://i.ibb.co/6RN9f482/P2.jpg"},
        {"id": "P024", "name": "Maya Pillai", "age": 40, "gender": "Female", "weight": 67, "bg": "AB-", "addr": "Solar Road", "state": "Bhubaneswar", "phone": 4321098765, "email": "maya.pillai@email.com", "admit": "2023-09-15", "disch": "2023-09-25", "status": "Discharged", "img": "https://i.ibb.co/gL9c0QTx/P1-1.jpg"},
        {"id": "P025", "name": "Prakash Jha", "age": 59, "gender": "Male", "weight": 82, "bg": "B+", "addr": "Lunar Avenue", "state": "Agra", "phone": 3210987654, "email": "prakash.jha@email.com", "admit": "2023-09-20", "disch": "2023-09-30", "status": "Discharged", "img": "https://i.ibb.co/4ZXXPz6S/P4.jpg"},
        {"id": "P026", "name": "Geeta Singh", "age": 31, "gender": "Female", "weight": 59, "bg": "O+", "addr": "Star Street", "state": "Mysore", "phone": 2109876543, "email": "geeta.singh@email.com", "admit": "2023-10-01", "disch": None, "status": "Admitted", "img": "https://i.ibb.co/spTJqyKK/P3-1.jpg"},
        {"id": "P027", "name": "Nitin Mehra", "age": 54, "gender": "Male", "weight": 78, "bg": "AB+", "addr": "Planet Road", "state": "Dehradun", "phone": 1098765432, "email": "nitin.mehra@email.com", "admit": "2023-10-05", "disch": "2023-10-15", "status": "Discharged", "img": "https://i.ibb.co/6RN9f482/P2.jpg"},
        {"id": "P028", "name": "Lata Iyer", "age": 29, "gender": "Female", "weight": 62, "bg": "A-", "addr": "Cosmic Lane", "state": "Jammu", "phone": 9876543210, "email": "lata.iyer@email.com", "admit": "2023-10-10", "disch": "2023-10-18", "status": "Discharged", "img": "https://i.ibb.co/S15ts9X/p-m3.jpg"},
        {"id": "P029", "name": "Santosh Nair", "age": 62, "gender": "Male", "weight": 76, "bg": "O-", "addr": "Astral Avenue", "state": "Shimla", "phone": 8765432109, "email": "santosh.nair@email.com", "admit": "2023-10-15", "disch": None, "status": "Admitted", "img": "https://i.ibb.co/6RN9f482/P2.jpg"},
        {"id": "P030", "name": "Divya Menon", "age": 42, "gender": "Female", "weight": 68, "bg": "B-", "addr": "Celestial Road", "state": "Pondicherry", "phone": 7654321098, "email": "divya.menon@email.com", "admit": "2023-10-20", "disch": "2023-10-28", "status": "Discharged", "img": "https://i.ibb.co/S15ts9X/p-m3.jpg"},
    ]

    records = []
    for p in patient_records:
        admit_dt = datetime.strptime(p["admit"], "%Y-%m-%d")
        disch_dt = datetime.strptime(p["disch"], "%Y-%m-%d") if p["disch"] else None

        records.append({
            "patient_id": mess_string(p["id"]),
            "name": mess_string(p["name"]),
            "age": int(p["age"]),                      # Pure numeric
            "gender": mess_string(p["gender"]),
            "weight": int(p["weight"]),                # Pure numeric
            "blood_group": mess_string(p["bg"]),
            "address": mess_string(p["addr"]),
            "state": mess_string(p["state"]),
            "phone": int(p["phone"]),                  # Pure numeric
            "email": mess_string(p["email"]),
            "admission_date": format_mixed_date(admit_dt),
            "discharge_date": format_mixed_date(disch_dt) if disch_dt else None,
            "status": mess_string(p["status"]),
            "Img": p["img"],
        })

    df = pd.DataFrame(records)

    # Inconsistent header names preserving the exact 14 columns
    header_map = {
        "patient_id": " Patient_ID ",
        "name": "Patient_Name",
        "age": " AGE ",
        "gender": "Gender",
        "weight": "Weight_KG ",
        "blood_group": " Blood_Group ",
        "address": "Address",
        "state": " State ",
        "phone": "Phone_Number",
        "email": " Email_Address ",
        "admission_date": "Admission_Date",
        "discharge_date": " Discharge_Date ",
        "status": "STATUS",
        "Img": " Img ",
    }
    df.rename(columns=header_map, inplace=True)

    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    df.to_excel(filepath, index=False)