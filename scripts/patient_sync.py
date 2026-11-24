import os
import pandas as pd
from generators.patient_generator import generate_patients


def get_available_patient_data(target_dir):
    """
    Dynamically loads patient records from the destination directory.
    If uncleaned_patient.xlsx does not exist yet, it generates it first.
    Returns:
        all_patient_ids: list of cleaned IDs (e.g., ['P001', 'P002', ...])
        admitted_patient_ids: list of IDs where status == 'Admitted'
    """
    possible_files = [
        os.path.join(target_dir, "uncleaned_patient.xlsx"),
        os.path.join(target_dir, "patient.xlsx"),
    ]
    
    patient_file = None
    for f in possible_files:
        if os.path.exists(f):
            patient_file = f
            break

    # If patient table hasn't been generated yet, generate it now
    if patient_file is None:
        patient_file = os.path.join(target_dir, "uncleaned_patient.xlsx")
        generate_patients(patient_file)

    # Read the patient file
    df = pd.read_excel(patient_file)

    # Normalize column names to locate patient_id and status regardless of messy headers
    col_map = {col: col.strip().lower().replace(" ", "_") for col in df.columns}
    df_renamed = df.rename(columns=col_map)

    # Find patient_id column
    p_col = [c for c in df_renamed.columns if "patient_id" in c or "patient" in c][0]
    
    # Strip whitespace and normalize to uppercase
    patient_ids = (
        df_renamed[p_col]
        .dropna()
        .astype(str)
        .str.strip()
        .str.upper()
        .tolist()
    )

    # Identify currently admitted patients if status column exists
    status_cols = [c for c in df_renamed.columns if "status" in c]
    if status_cols:
        s_col = status_cols[0]
        admitted_ids = (
            df_renamed[df_renamed[s_col].astype(str).str.strip().str.title() == "Admitted"][p_col]
            .astype(str)
            .str.strip()
            .str.upper()
            .tolist()
        )
    else:
        admitted_ids = patient_ids[:8]

    return patient_ids, admitted_ids