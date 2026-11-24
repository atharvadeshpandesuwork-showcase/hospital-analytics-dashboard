# Insert doctors patient
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Configuaration
# Replace these with your actual MySQL Workbench / MySQL Server credentials
DB_USER = "root"
DB_PASSWORD = "root%40123"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "hospital_db"


# File configuration
EXCEL_FILE = "Cleaned Data/patient.xlsx"
SHEET_NAME = "Sheet1"
TABLE_NAME = "patient"

# Connection string
# Format: mysql+pymysql://username:password@host:port/database_name
connection_string = (f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    print("Attempting to connect to MySQL Server...")
    engine = create_engine(connection_string)

    # Test the connection by opening a temporary connection context
    with engine.connect() as connection:
        print(" Connection successful!\n")

    # --- 4. READ EXCEL & INSERT INTO MYSQL ---
    print(f"Reading data from '{EXCEL_FILE}'...")
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

    print(f"Inserting {len(df)} rows into MySQL table '{TABLE_NAME}'...")
    df.to_sql(
        name=TABLE_NAME,
        con=engine,
        if_exists="replace",  # Options: 'fail', 'replace', 'append'
        index=False,  # Set to True if you want the DataFrame index as a column
    )

    print(
        f" Successfully created/updated table '{TABLE_NAME}' and inserted all data!"
    )

except SQLAlchemyError as e:
    print("\n Connection Failed or Database Error Occurred:")
    print(e)
except FileNotFoundError:
    print(
        f"\n Error: The Excel file '{EXCEL_FILE}' was not found. Please check the path."
    )
except Exception as e:
    print(f"\n An unexpected error occurred: {e}")