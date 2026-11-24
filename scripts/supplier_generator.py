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


def generate_suppliers(filepath, seed=42):
    """
    Generates synthetic pharmaceutical supplier records strictly preserving the exact 12 columns
    from Supplier.xlsx, including column-shift discrepancies and messy text formatting.
    """
    if seed:
        random.seed(seed)

    suppliers_base = [
        {
            "id": "SUP001",
            "name": "MediPharm Distributors",
            "contact": "Rajesh Gupta",
            "phone": 9876543210,
            "email": "rajesh@medipharm.com",
            "addr": 'Phase 1"',
            "city": "Industrial Area",
            "state": 'Phase 1"',
            "pin": 110001,
            "state_1": "Delhi",
            "start": "2023-01-01",
            "end": "2024-12-31",
        },
        {
            "id": "SUP002",
            "name": "HealthCare Supplies",
            "contact": "Priya Sharma",
            "phone": 8765432109,
            "email": "priya@healthcaresupplies.com",
            "addr": 'Sector 5"',
            "city": "Business Park",
            "state": 'Sector 5"',
            "pin": 400001,
            "state_1": "Maharashtra",
            "start": "2023-01-15",
            "end": "2024-12-31",
        },
        {
            "id": "SUP003",
            "name": "MediCore Enterprises",
            "contact": "Amit Kumar",
            "phone": 7654321098,
            "email": "amit@medicore.com",
            "addr": 'Zone 3"',
            "city": "Corporate Hub",
            "state": 'Zone 3"',
            "pin": 560001,
            "state_1": "Karnataka",
            "start": "2023-02-01",
            "end": "2024-12-31",
        },
        {
            "id": "SUP004",
            "name": "LifeLine Pharmaceuticals",
            "contact": "Sneha Patel",
            "phone": 6543210987,
            "email": "sneha@lifeline.com",
            "addr": 'Block B"',
            "city": "Pharma Valley",
            "state": 'Block B"',
            "pin": 600001,
            "state_1": "Tamil Nadu",
            "start": "2023-02-15",
            "end": "2024-12-31",
        },
        {
            "id": "SUP005",
            "name": "MediTech Solutions",
            "contact": "Vikram Singh",
            "phone": 5432109876,
            "email": "vikram@meditech.com",
            "addr": 'Area 7"',
            "city": "Tech Park",
            "state": 'Area 7"',
            "pin": 500001,
            "state_1": "Telangana",
            "start": "2023-03-01",
            "end": "2024-12-31",
        },
    ]

    records = []
    for sup in suppliers_base:
        s_dt = datetime.strptime(sup["start"], "%Y-%m-%d")
        e_dt = datetime.strptime(sup["end"], "%Y-%m-%d")

        records.append({
            "supplier_id": mess_string(sup["id"]),
            "name": mess_string(sup["name"]),
            "contact_person": mess_string(sup["contact"]),
            "phone": int(sup["phone"]),                                # Numeric intact
            "email": mess_string(sup["email"]),
            "address": mess_string(sup["addr"]),
            "city": mess_string(sup["city"]),
            "state": mess_string(sup["state"]),
            "pincode": int(sup["pin"]),                                # Numeric intact
            "state.1": mess_string(sup["state_1"]),
            "contract_start_date": format_mixed_date(s_dt),
            "contract_end_date": format_mixed_date(e_dt),
        })

    df = pd.DataFrame(records)

    # Inconsistent header names preserving the exact 12 columns
    header_map = {
        "supplier_id": " SUPPLIER_ID ",
        "name": "Supplier_Name",
        "contact_person": "Contact_Person ",
        "phone": "Phone_Number",
        "email": " Email_Address ",
        "address": " Address ",
        "city": "City",
        "state": "State",
        "pincode": " PINCODE ",
        "state.1": "state.1",
        "contract_start_date": "Contract_Start_Date ",
        "contract_end_date": " contract_end_date ",
    }
    df.rename(columns=header_map, inplace=True)

    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    df.to_excel(filepath, index=False)