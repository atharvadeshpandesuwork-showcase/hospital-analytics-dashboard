import os
import random
from datetime import datetime
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


def generate_doctors(filepath, seed=42):
    if seed:
        random.seed(seed)

    doctors_base = [
        {
            "id": "D001",
            "name": "Dr. Aditya Gupta",
            "spec": "Cardiologist",
            "dept": "Cardiology",
            "sal": 150000,
            "status": "Active",
            "avail": "Available",
            "join": "2015-06-01",
            "qual": "MD",
            "exp": 12,
            "phone": "9876543210",
            "email": "aditya.gupta@hospital.com",
            "img": "https://i.ibb.co/r2Vyh5MX/Dr-6.jpg",
        },
        {
            "id": "D002",
            "name": "Dr. Neha Verma",
            "spec": "Neurologist",
            "dept": "Neurology",
            "sal": 145000,
            "status": "Active",
            "avail": "Available",
            "join": "2016-07-15",
            "qual": "MD",
            "exp": 10,
            "phone": "8765432109",
            "email": "neha.verma@hospital.com",
            "img": "https://i.ibb.co/jkYD4jsY/DR-5-1.jpg",
        },
        {
            "id": "D003",
            "name": "Dr. Rajesh Kumar",
            "spec": "Orthopedic Surgeon",
            "dept": "Orthopedics",
            "sal": 140000,
            "status": "Active",
            "avail": "On Leave",
            "join": "2015-08-20",
            "qual": "MS",
            "exp": 11,
            "phone": "7654321098",
            "email": "rajesh.kumar@hospital.com",
            "img": "https://i.ibb.co/8D1NnQFm/DR-5.jpg",
        },
        {
            "id": "D004",
            "name": "Dr. Priya Sharma",
            "spec": "Gynecologist",
            "dept": "Gynecology",
            "sal": 135000,
            "status": "Active",
            "avail": "Available",
            "join": "2017-01-10",
            "qual": "MBBS",
            "exp": 8,
            "phone": "6543210987",
            "email": "priya.sharma@hospital.com",
            "img": "https://i.ibb.co/bjnbLqRw/DR-4.jpg",
        },
        {
            "id": "D005",
            "name": "Dr. Vikram Singh",
            "spec": "Pediatrician",
            "dept": "Pediatrics",
            "sal": 130000,
            "status": "Active",
            "avail": "Available",
            "join": "2016-03-05",
            "qual": "MD (Pediatrics)",
            "exp": 9,
            "phone": "5432109876",
            "email": "vikram.singh@hospital.com",
            "img": "https://i.ibb.co/gFzShn7G/DR-3.jpg",
        },
        {
            "id": "D006",
            "name": "Dr. Anita Patel",
            "spec": "Dermatologist",
            "dept": "Dermatology",
            "sal": 125000,
            "status": "Active",
            "avail": "Available",
            "join": "2018-02-15",
            "qual": "MD (Dermatology)",
            "exp": 7,
            "phone": "4321098765",
            "email": "anita.patel@hospital.com",
            "img": "https://i.ibb.co/7NQdkhRx/DR-2.jpg",
        },
        {
            "id": "D007",
            "name": "Dr. Suresh Nair",
            "spec": "Gastroenterologist",
            "dept": "Gastroenterology",
            "sal": 155000,
            "status": "Active",
            "avail": "On Leave",
            "join": "2014-05-20",
            "qual": "MD",
            "exp": 13,
            "phone": "3210987654",
            "email": "suresh.nair@hospital.com",
            "img": "https://i.ibb.co/5g6N8dwD/DR-1.jpg",
        },
        {
            "id": "D008",
            "name": "Dr. Kavita Menon",
            "spec": "Ophthalmologist",
            "dept": "Ophthalmology",
            "sal": 120000,
            "status": "Active",
            "avail": "Available",
            "join": "2019-04-10",
            "qual": "MS (Ophthalmology)",
            "exp": 6,
            "phone": "2109876543",
            "email": "kavita.menon@hospital.com",
            "img": "https://i.ibb.co/r2Vyh5MX/Dr-6.jpg",
        },
        {
            "id": "D009",
            "name": "Dr. Deepak Joshi",
            "spec": "ENT Specialist",
            "dept": "ENT",
            "sal": 115000,
            "status": "Active",
            "avail": "Available",
            "join": "2020-06-25",
            "qual": "MS (ENT)",
            "exp": 5,
            "phone": "9123456780",
            "email": "deepak.joshi@hospital.com",
            "img": "https://i.ibb.co/jkYD4jsY/DR-5-1.jpg",
        },
        {
            "id": "D010",
            "name": "Dr. Meera Reddy",
            "spec": "Psychiatrist",
            "dept": "Psychiatry",
            "sal": 130000,
            "status": "Active",
            "avail": "Available",
            "join": "2017-08-15",
            "qual": "MD (Psychiatry)",
            "exp": 8,
            "phone": "8234567891",
            "email": "meera.reddy@hospital.com",
            "img": "https://i.ibb.co/8D1NnQFm/DR-5.jpg",
        },
        {
            "id": "D011",
            "name": "Dr. Sanjay Malhotra",
            "spec": "Urologist",
            "dept": "Urology",
            "sal": 145000,
            "status": "Active",
            "avail": "Available",
            "join": "2015-09-30",
            "qual": "MS",
            "exp": 11,
            "phone": "8765432119",
            "email": "sanjay.malhotra@hospital.com",
            "img": "https://i.ibb.co/bjnbLqRw/DR-4.jpg",
        },
        {
            "id": "D012",
            "name": "Dr. Pooja Das",
            "spec": "Endocrinologist",
            "dept": "Endocrinology",
            "sal": 140000,
            "status": "Active",
            "avail": "On Leave",
            "join": "2016-11-20",
            "qual": "MD",
            "exp": 10,
            "phone": "7654321108",
            "email": "pooja.das@hospital.com",
            "img": "https://i.ibb.co/gFzShn7G/DR-3.jpg",
        },
        {
            "id": "D013",
            "name": "Dr. Amit Khanna",
            "spec": "Nephrologist",
            "dept": "Nephrology",
            "sal": 150000,
            "status": "Active",
            "avail": "Available",
            "join": "2014-10-15",
            "qual": "MD",
            "exp": 12,
            "phone": "6543210997",
            "email": "amit.khanna@hospital.com",
            "img": "https://i.ibb.co/7NQdkhRx/DR-2.jpg",
        },
        {
            "id": "D014",
            "name": "Dr. Sonali Bhatia",
            "spec": "Pulmonologist",
            "dept": "Pulmonology",
            "sal": 135000,
            "status": "Active",
            "avail": "Available",
            "join": "2017-05-05",
            "qual": "MD (Pulmonology)",
            "exp": 8,
            "phone": "5432109886",
            "email": "sonali.bhatia@hospital.com",
            "img": "https://i.ibb.co/5g6N8dwD/DR-1.jpg",
        },
        {
            "id": "D015",
            "name": "Dr. Ravi Mehta",
            "spec": "Oncologist",
            "dept": "Oncology",
            "sal": 160000,
            "status": "Active",
            "avail": "Available",
            "join": "2013-03-10",
            "qual": "MD",
            "exp": 14,
            "phone": "4321098775",
            "email": "ravi.mehta@hospital.com",
            "img": "https://i.ibb.co/5g6N8dwD/DR-1.jpg",
        },
    ]

    records = []
    for d in doctors_base:
        joining_dt = datetime.strptime(d["join"], "%Y-%m-%d")
        records.append(
            {
                "doctor_id": mess_string(d["id"]),
                "name": mess_string(d["name"]),
                "specialization": mess_string(d["spec"]),
                "department": mess_string(d["dept"]),
                "salary": int(d["sal"]),
                "status": mess_string(d["status"]),
                "availability": mess_string(d["avail"]),
                "joining_date": format_mixed_date(joining_dt),
                "qualification": mess_string(d["qual"]),
                "experience_years": int(d["exp"]),
                "phone": mess_string(d["phone"]),
                "email": mess_string(d["email"]),
                "Img": d["img"],
            }
        )

    df = pd.DataFrame(records).rename(
        columns={
            "doctor_id": " Doctor_ID ",
            "name": "Doctor_Name",
            "specialization": " SPECIALIZATION",
            "department": "Department ",
            "salary": "SALARY",
            "status": " Status ",
            "availability": "availability ",
            "joining_date": " Joining_Date ",
            "qualification": "Qualification",
            "experience_years": "Experience_Years ",
            "phone": " Phone_Number ",
            "email": "Email_Address",
            "Img": " Img ",
        }
    )
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    df.to_excel(filepath, index=False)