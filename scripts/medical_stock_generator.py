import os
import random
from datetime import datetime, timedelta
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


def generate_medical_stock(filepath, seed=42):
    if seed:
        random.seed(seed)

    medicines = [
        {
            "id": "MED001",
            "name": "Paracetamol",
            "cat": "Pain Relief",
            "sup": "SUP001",
            "cost": 2.5,
            "unit": 5,
            "qty": 500,
            "mfg": "2023-01-15",
            "exp": "2024-12-31",
            "batch": "BT12345",
            "reorder": 100,
        },
        {
            "id": "MED002",
            "name": "Amoxicillin",
            "cat": "Antibiotic",
            "sup": "SUP002",
            "cost": 5.0,
            "unit": 10,
            "qty": 300,
            "mfg": "2023-02-20",
            "exp": "2024-06-30",
            "batch": "BT23456",
            "reorder": 50,
        },
        {
            "id": "MED003",
            "name": "Omeprazole",
            "cat": "Antacid",
            "sup": "SUP003",
            "cost": 4.0,
            "unit": 8,
            "qty": 400,
            "mfg": "2023-03-10",
            "exp": "2025-03-31",
            "batch": "BT34567",
            "reorder": 75,
        },
        {
            "id": "MED004",
            "name": "Loratadine",
            "cat": "Antihistamine",
            "sup": "SUP001",
            "cost": 3.0,
            "unit": 6,
            "qty": 350,
            "mfg": "2023-01-25",
            "exp": "2024-09-30",
            "batch": "BT45678",
            "reorder": 60,
        },
        {
            "id": "MED005",
            "name": "Metformin",
            "cat": "Antidiabetic",
            "sup": "SUP002",
            "cost": 3.5,
            "unit": 7,
            "qty": 250,
            "mfg": "2023-02-15",
            "exp": "2024-08-31",
            "batch": "BT56789",
            "reorder": 40,
        },
        {
            "id": "MED006",
            "name": "Atorvastatin",
            "cat": "Cholesterol",
            "sup": "SUP003",
            "cost": 6.0,
            "unit": 12,
            "qty": 200,
            "mfg": "2023-03-05",
            "exp": "2024-07-31",
            "batch": "BT67890",
            "reorder": 35,
        },
        {
            "id": "MED007",
            "name": "Salbutamol",
            "cat": "Bronchodilator",
            "sup": "SUP001",
            "cost": 4.5,
            "unit": 9,
            "qty": 180,
            "mfg": "2023-01-30",
            "exp": "2024-11-30",
            "batch": "BT78901",
            "reorder": 30,
        },
        {
            "id": "MED008",
            "name": "Amlodipine",
            "cat": "Antihypertensive",
            "sup": "SUP002",
            "cost": 5.5,
            "unit": 11,
            "qty": 220,
            "mfg": "2023-02-25",
            "exp": "2024-10-31",
            "batch": "BT89012",
            "reorder": 40,
        },
        {
            "id": "MED009",
            "name": "Diazepam",
            "cat": "Sedative",
            "sup": "SUP003",
            "cost": 7.0,
            "unit": 14,
            "qty": 150,
            "mfg": "2023-03-15",
            "exp": "2024-05-31",
            "batch": "BT90123",
            "reorder": 25,
        },
        {
            "id": "MED010",
            "name": "Insulin",
            "cat": "Antidiabetic",
            "sup": "SUP001",
            "cost": 15.0,
            "unit": 30,
            "qty": 100,
            "mfg": "2023-01-20",
            "exp": "2024-04-30",
            "batch": "BT01234",
            "reorder": 20,
        },
        {
            "id": "MED011",
            "name": "Ibuprofen",
            "cat": "Pain Relief",
            "sup": "SUP002",
            "cost": 3.0,
            "unit": 6,
            "qty": 450,
            "mfg": "2023-02-10",
            "exp": "2025-01-31",
            "batch": "BT12345",
            "reorder": 90,
        },
        {
            "id": "MED012",
            "name": "Cetirizine",
            "cat": "Antihistamine",
            "sup": "SUP003",
            "cost": 2.5,
            "unit": 5,
            "qty": 380,
            "mfg": "2023-03-20",
            "exp": "2024-08-31",
            "batch": "BT23456",
            "reorder": 70,
        },
        {
            "id": "MED013",
            "name": "Ceftriaxone",
            "cat": "Antibiotic",
            "sup": "SUP001",
            "cost": 8.0,
            "unit": 16,
            "qty": 120,
            "mfg": "2023-01-10",
            "exp": "2024-03-31",
            "batch": "BT34567",
            "reorder": 20,
        },
        {
            "id": "MED014",
            "name": "Simvastatin",
            "cat": "Cholesterol",
            "sup": "SUP002",
            "cost": 5.5,
            "unit": 11,
            "qty": 180,
            "mfg": "2023-02-05",
            "exp": "2025-02-28",
            "batch": "BT45678",
            "reorder": 30,
        },
        {
            "id": "MED015",
            "name": "Ranitidine",
            "cat": "Antacid",
            "sup": "SUP003",
            "cost": 4.0,
            "unit": 8,
            "qty": 250,
            "mfg": "2023-03-25",
            "exp": "2024-06-30",
            "batch": "BT56789",
            "reorder": 45,
        },
    ]

    records = []
    for m in medicines:
        mfg_dt = datetime.strptime(m["mfg"], "%Y-%m-%d")
        exp_dt = datetime.strptime(m["exp"], "%Y-%m-%d")

        records.append(
            {
                "medicine_id": mess_string(m["id"]),
                "name": mess_string(m["name"]),
                "category": mess_string(m["cat"]),
                "supplier_id": mess_string(m["sup"]),
                "cost_price": float(m["cost"]),
                "unit_price": int(m["unit"]),
                "stock_qty": int(m["qty"]),
                "expiry_date": format_mixed_date(exp_dt),
                "manufacture_date": format_mixed_date(mfg_dt),
                "batch_number": mess_string(m["batch"]),
                "reorder_level": int(m["reorder"]),
            }
        )

    df = pd.DataFrame(records)

    # Inconsistent header names preserving the exact 11 columns
    header_map = {
        "medicine_id": " MEDICINE_ID ",
        "name": "Medicine_Name",
        "category": " CATEGORY",
        "supplier_id": "Supplier_Id ",
        "cost_price": "Cost_Price ",
        "unit_price": "UNIT_PRICE",
        "stock_qty": " stock_qty ",
        "expiry_date": " Expiry_Date ",
        "manufacture_date": "Manufacture_Date",
        "batch_number": " BATCH_NUMBER ",
        "reorder_level": "reorder_level ",
    }
    df.rename(columns=header_map, inplace=True)

    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    df.to_excel(filepath, index=False)