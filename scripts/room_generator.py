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


def generate_rooms(filepath, seed=42):
    """
    Generates synthetic hospital rooms preserving the exact 8 columns
    from Rooms.xlsx, matching department floor distributions and messy text formatting.
    """
    if seed:
        random.seed(seed)

    rooms_base = [
        {"id": "R001", "dept": "DEPT001", "type": "General", "floor": 3, "cap": 4, "status": "Available", "charge": 1000, "maint": 1000},
        {"id": "R002", "dept": "DEPT001", "type": "Private", "floor": 3, "cap": 1, "status": "Occupied", "charge": 3000, "maint": 3000},
        {"id": "R003", "dept": "DEPT001", "type": "ICU", "floor": 3, "cap": 1, "status": "Available", "charge": 5000, "maint": 5000},
        {"id": "R004", "dept": "DEPT002", "type": "General", "floor": 4, "cap": 4, "status": "Available", "charge": 1000, "maint": 1000},
        {"id": "R005", "dept": "DEPT002", "type": "Private", "floor": 4, "cap": 1, "status": "Occupied", "charge": 3000, "maint": 3000},
        {"id": "R006", "dept": "DEPT002", "type": "ICU", "floor": 4, "cap": 1, "status": "Available", "charge": 5000, "maint": 5000},
        {"id": "R007", "dept": "DEPT003", "type": "General", "floor": 2, "cap": 4, "status": "Available", "charge": 1000, "maint": 1000},
        {"id": "R008", "dept": "DEPT003", "type": "Private", "floor": 2, "cap": 1, "status": "Occupied", "charge": 3000, "maint": 3000},
        {"id": "R009", "dept": "DEPT003", "type": "ICU", "floor": 2, "cap": 1, "status": "Available", "charge": 5000, "maint": 5000},
        {"id": "R010", "dept": "DEPT004", "type": "General", "floor": 5, "cap": 4, "status": "Available", "charge": 1000, "maint": 1000},
        {"id": "R011", "dept": "DEPT004", "type": "Private", "floor": 5, "cap": 1, "status": "Occupied", "charge": 3000, "maint": 3000},
        {"id": "R012", "dept": "DEPT004", "type": "ICU", "floor": 5, "cap": 1, "status": "Available", "charge": 5000, "maint": 5000},
        {"id": "R013", "dept": "DEPT005", "type": "General", "floor": 1, "cap": 4, "status": "Available", "charge": 1000, "maint": 1000},
        {"id": "R014", "dept": "DEPT005", "type": "Private", "floor": 1, "cap": 1, "status": "Occupied", "charge": 3000, "maint": 3000},
        {"id": "R015", "dept": "DEPT005", "type": "ICU", "floor": 1, "cap": 1, "status": "Available", "charge": 5000, "maint": 5000},
        {"id": "R016", "dept": "DEPT006", "type": "General", "floor": 3, "cap": 4, "status": "Available", "charge": 1000, "maint": 1000},
        {"id": "R017", "dept": "DEPT006", "type": "Private", "floor": 3, "cap": 1, "status": "Occupied", "charge": 3000, "maint": 3000},
        {"id": "R018", "dept": "DEPT007", "type": "General", "floor": 4, "cap": 4, "status": "Available", "charge": 1000, "maint": 1000},
        {"id": "R019", "dept": "DEPT007", "type": "Private", "floor": 4, "cap": 1, "status": "Occupied", "charge": 3000, "maint": 3000},
        {"id": "R020", "dept": "DEPT007", "type": "ICU", "floor": 4, "cap": 1, "status": "Available", "charge": 5000, "maint": 5000},
        {"id": "R021", "dept": "DEPT008", "type": "General", "floor": 2, "cap": 4, "status": "Available", "charge": 1000, "maint": 1000},
        {"id": "R022", "dept": "DEPT008", "type": "Private", "floor": 2, "cap": 1, "status": "Occupied", "charge": 3000, "maint": 3000},
        {"id": "R023", "dept": "DEPT009", "type": "General", "floor": 5, "cap": 4, "status": "Available", "charge": 1000, "maint": 1000},
        {"id": "R024", "dept": "DEPT009", "type": "Private", "floor": 5, "cap": 1, "status": "Occupied", "charge": 3000, "maint": 3000},
        {"id": "R025", "dept": "DEPT010", "type": "General", "floor": 6, "cap": 4, "status": "Available", "charge": 1000, "maint": 1000},
    ]

    records = []
    for r in rooms_base:
        records.append({
            "room_id": mess_string(r["id"]),
            "department_id": mess_string(r["dept"]),
            "room_type": mess_string(r["type"]),
            "floor": int(r["floor"]),                                    # Intact numeric
            "capacity": int(r["cap"]),                                  # Intact numeric
            "status": mess_string(r["status"]),
            "daily_charge": int(r["charge"]),                           # Intact numeric
            "avg montly maintenance cost": int(r["maint"]),              # Intact numeric
        })

    df = pd.DataFrame(records)

    # Inconsistent header names preserving the exact 8 columns
    header_map = {
        "room_id": " ROOM_ID ",
        "department_id": "department_id ",
        "room_type": " Room_Type ",
        "floor": "FLOOR",
        "capacity": " Capacity ",
        "status": " STATUS ",
        "daily_charge": "daily_charge",
        "avg montly maintenance cost": " Avg_Monthly_Maintenance_Cost ",
    }
    df.rename(columns=header_map, inplace=True)

    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    df.to_excel(filepath, index=False)