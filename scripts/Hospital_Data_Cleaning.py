# Hospital Data Cleaning
# Converted from Hospital_Data_Cleaning.ipynb
# Original code cells are kept in notebook order.


# ====================================================================
# NOTEBOOK CELL 1
# ====================================================================
import numpy as np
import pandas as pd

# ====================================================================
# NOTEBOOK CELL 2
# ====================================================================
df_appointment = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_appointments.xlsx')
df_appointment.head(10)

# ====================================================================
# NOTEBOOK CELL 3
# ====================================================================
# Cleaning All column Names
df_appointment.columns = df_appointment.columns.str.strip().str.title()
df_appointment.columns = df_appointment.columns.str.replace(r'\s+', '')

# ====================================================================
# NOTEBOOK CELL 4
# ====================================================================
# Cleaning Appointment__id Column
df_appointment['Appointment_Id'] = df_appointment['Appointment_Id'].str.strip()
df_appointment['Appointment_ID'] = df_appointment['Appointment_Id'].str[:3].str.upper()
df_appointment['Appointment_ID'] = df_appointment['Appointment_ID'].str.replace(r'\s+', '')


# Dropping Appointment_ID column
df_appointment.drop(columns = 'Appointment_ID',inplace = True)

# Cleaning Patient_Id column
df_appointment['Patient_Id'] = df_appointment['Patient_Id'].str.strip()
df_appointment['Patient_Id'] = df_appointment['Patient_Id'].str.replace(r'\s+', '')
df_appointment['Patient_Id'] = df_appointment['Patient_Id'].str.capitalize()


# Cleaning Doctor_Id column
df_appointment['Doctor_Id'] = df_appointment['Doctor_Id'].str.strip()
df_appointment['Doctor_Id'] = df_appointment['Doctor_Id'].str.replace(r'\s+', '')
df_appointment['Doctor_Id'] = df_appointment['Doctor_Id'].str.capitalize()


# Cleaning Status Column
df_appointment['Status'] = df_appointment['Status'].str.strip()
df_appointment['Status'] = df_appointment['Status'].str.replace(r'\s+', '')
df_appointment['Status'] = df_appointment['Status'].str.capitalize()

# Cleaning Reason column
df_appointment['Reason'] = df_appointment['Reason'].str.strip()
df_appointment['Reason'] = df_appointment['Reason'].str.title()

# Cleaning Notes Column
df_appointment['Notes'] = df_appointment['Notes'].str.strip()
df_appointment['Notes'] = df_appointment['Notes'].str.capitalize()

# Cleaning Notes Column
df_appointment['Suggest'] = df_appointment['Suggest'].str.strip()
df_appointment['Suggest'] = df_appointment['Suggest'].str.capitalize()

# Cleaning Payment_Method column
df_appointment['Payment_Method'] = df_appointment['Payment_Method'].str.strip()
df_appointment['Payment_Method'] = df_appointment['Payment_Method'].str.capitalize()

# Cleaning Disgnosis column
df_appointment['Diagnosis'] = df_appointment['Diagnosis'].str.strip()
df_appointment['Diagnosis'] = df_appointment['Diagnosis'].str.capitalize()

df_appointment.head(5)

# ====================================================================
# NOTEBOOK CELL 5
# ====================================================================
# Assigning None to blank cells where apoint is cancelled
df_appointment.loc[df_appointment['Status'] == 'Cancelled','Suggest'] = df_appointment.loc[df_appointment['Status'] == 'Cancelled','Suggest'].fillna('None')
df_appointment.loc[df_appointment['Suggest'] == 'None']

# ====================================================================
# NOTEBOOK CELL 6
# ====================================================================
# Cleaning Appointment Date
df_appointment['Appointment_Date'] = df_appointment['Appointment_Date'].str.strip()
df_appointment['Appointment_Date'] = pd.to_datetime(df_appointment['Appointment_Date'],format = 'mixed')
df_appointment['Appointment_Date'].dt.strftime('%Y-%m-%d')

# Cleaning Appointment Time
df_appointment['Appointment_Time'] = df_appointment['Appointment_Time'].str.strip()
df_appointment['Appointment_Time'] = pd.to_datetime(df_appointment['Appointment_Time'])
df_appointment['Appointment_Time'] = df_appointment['Appointment_Time'].dt.strftime('%H:%M:%S')

df_appointment.head(5)

# ====================================================================
# NOTEBOOK CELL 7
# ====================================================================
# Reading beds Data
df_bed = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_beds.xlsx')
df_bed.head(5)

# ====================================================================
# NOTEBOOK CELL 8
# ====================================================================
# Cleaning beds data
df_bed.columns = df_bed.columns.str.strip().str.title()
df_bed['Bed_Id'] = df_bed['Bed_Id'].str.strip()
df_bed['Bed_Id'] = df_bed['Bed_Id'].str.capitalize()

df_bed['Room_Id'] = df_bed['Room_Id'].str.strip()
df_bed['Room_Id'] = df_bed['Room_Id'].str.capitalize()

df_bed['Status'] = df_bed['Status'].str.strip()
df_bed['Status'] = df_bed['Status'].str.capitalize()

df_bed['Patient_Id'] = df_bed['Patient_Id'].str.strip()
df_bed['Patient_Id'] = df_bed['Patient_Id'].str.capitalize()

df_bed['Occupied_From'] = pd.to_datetime(df_bed['Occupied_From'],format = "mixed")
df_bed['Occupied_From'] = df_bed['Occupied_From'].dt.strftime('%Y-%m-%d')

df_bed['Occupied_Till'] = pd.to_datetime(df_bed['Occupied_Till'],format = "mixed")
df_bed['Occupied_Till'] = df_bed['Occupied_Till'].dt.strftime('%Y-%m-%d')

df_bed.head(1)

# ====================================================================
# NOTEBOOK CELL 9
# ====================================================================
# Reading departments data
df_department = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_departments.xlsx')
df_department.head(5)

# ====================================================================
# NOTEBOOK CELL 10
# ====================================================================
# Cleaning departments columns

df_department.columns = df_department.columns.str.strip()
df_department.columns = df_department.columns.str.title()
df_department.head()

# ====================================================================
# NOTEBOOK CELL 11
# ====================================================================
# Cleaning department_id column
df_department['Department_Id'] = df_department['Department_Id'].str.strip()
df_department['Department_Id'] = df_department['Department_Id'].str.upper()
df_department['Department_Id'] = df_department['Department_Id'].str.replace(r'\s+', '')


# Cleaning Dept Name colummn
df_department['Dept_Name'] = df_department['Dept_Name'].str.strip()
df_department['Dept_Name'] = df_department['Dept_Name'].str.replace(r'\s+','')
df_department['Dept_Name'] = df_department['Dept_Name'].str.capitalize()

# Cleaning Head doctor id column
df_department['Head_Doctor_Id'] = df_department['Head_Doctor_Id'].str.strip()
df_department['Head_Doctor_Id'] = df_department['Head_Doctor_Id'].str.upper()

df_department.head(5)

# ====================================================================
# NOTEBOOK CELL 12
# ====================================================================
# Cleaning Doctors data
df_doctors = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_doctors.xlsx')
df_doctors.head(5)

# ====================================================================
# NOTEBOOK CELL 13
# ====================================================================
# Standardizng column names
df_doctors.columns = df_doctors.columns.str.strip()
df_doctors.columns = df_doctors.columns.str.title()
df_doctors.head(1)

# ====================================================================
# NOTEBOOK CELL 14
# ====================================================================
# Cleaning Doctor ID column
df_doctors['Doctor_Id'] = df_doctors['Doctor_Id'].str.strip()
df_doctors['Doctor_Id'] = df_doctors['Doctor_Id'].str.upper()

# Cleaning doctor name column
df_doctors['Doctor_Name'] = df_doctors['Doctor_Name'].str.strip()
df_doctors['Doctor_Name'] = df_doctors['Doctor_Name'].str.title()

# Cleaning specialization column
df_doctors['Specialization'] = df_doctors['Specialization'].str.strip()
df_doctors['Specialization'] = df_doctors['Specialization'].str.title()

# Cleaning department column
df_doctors['Department'] = df_doctors['Department'].str.strip()
df_doctors['Department'] = df_doctors['Department'].str.capitalize()

# Cleaning status column
df_doctors['Status'] = df_doctors['Status'].str.strip()
df_doctors['Status'] = df_doctors['Status'].str.capitalize()

# Cleaning Availability Column
df_doctors['Availability'] = df_doctors['Availability'].str.strip()
df_doctors['Availability'] = df_doctors['Availability'].str.title()

# Cleaning Joining Date column
df_doctors['Joining_Date'].str.strip()
df_doctors['Joining_Date'] = pd.to_datetime(df_doctors['Joining_Date'], format = 'mixed').dt.strftime('%Y-%m-%d')

# Cleaning Qualification Column
df_doctors['Qualification'] = df_doctors['Qualification'].str.strip()
df_doctors['Qualification'] = df_doctors['Qualification'].str.upper()
df_doctors['Qualification'] = df_doctors['Qualification'].replace('MD (PEDIATRICS)','MD (Pediatrics)')
df_doctors['Qualification'] = df_doctors['Qualification'].replace('MD (DERMATOLOGY)','MD (Dermatology)')
df_doctors['Qualification'] = df_doctors['Qualification'].replace('MS (OPHTHALMOLOGY)','MS (Ophthalmology)')
df_doctors['Qualification'] = df_doctors['Qualification'].replace('MD (PULMONOLOGY)','MD (Pulmonology)')
df_doctors['Qualification'] = df_doctors['Qualification'].replace('MD (PSYCHIATRY)','MD (Psychiatry)')

# Cleaning email address column
df_doctors['Email_Address'] = df_doctors['Email_Address'].str.strip()
df_doctors['Email_Address'] = df_doctors['Email_Address'].str.lower()

# Cleaning Phone Number
df_doctors['Phone_Number'] = pd.to_numeric(df_doctors['Phone_Number'])


df_doctors.head(5)

# ====================================================================
# NOTEBOOK CELL 15
# ====================================================================
# Cleaning Hospital Bills data
df_bills = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_hospital_bills.xlsx')

# ====================================================================
# NOTEBOOK CELL 16
# ====================================================================
# Standardizing columns
df_bills.columns = df_bills.columns.str.strip()
df_bills.columns = df_bills.columns.str.title()

# ====================================================================
# NOTEBOOK CELL 17
# ====================================================================
# Cleaning the Bill_Id column
df_bills['Bill_Id'] = df_bills['Bill_Id'].str.strip()
df_bills['Bill_Id'] = df_bills['Bill_Id'].str.upper()

# Cleaning Patient_Id column
df_bills['Patient_Id'] = df_bills['Patient_Id'].str.strip()
df_bills['Patient_Id'] = df_bills['Patient_Id'].str.upper()

# Cleaning admission date
df_bills['Admission_Date'] = pd.to_datetime(df_bills['Admission_Date'],format='mixed').dt.strftime('%Y-%m-%d')

# Cleaning discharge_date
df_bills['Discharge_Date'] = pd.to_datetime (df_bills['Discharge_Date'], format = 'mixed').dt.strftime('%Y-%m-%d')

# Cleaning Payment Status column
df_bills['Payment_Status'] = df_bills['Payment_Status'].str.strip().str.capitalize()

# Cleaning Payment method column
df_bills['Payment_Method'] = df_bills['Payment_Method'].str.strip().str.capitalize()

df_bills.head(5)

# ====================================================================
# NOTEBOOK CELL 18
# ====================================================================
# Cleaning medical stock data
df_medical_stock = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_medical_stock.xlsx')

# ====================================================================
# NOTEBOOK CELL 19
# ====================================================================
# Standardizing columns
df_medical_stock.columns = df_medical_stock.columns.str.strip().str.title()

# Cleaning Medicine_Id column
df_medical_stock['Medicine_Id'] = df_medical_stock['Medicine_Id'].str.strip().str.upper()

# Cleaning Medicine Name column
df_medical_stock['Medicine_Name'] = df_medical_stock['Medicine_Name'].str.strip().str.capitalize()

# Cleaning Category column
df_medical_stock['Category'] = df_medical_stock['Category'].str.strip().str.title()

# Cleaning Supplier Id column
df_medical_stock['Supplier_Id'] = df_medical_stock['Supplier_Id'].str.strip().str.upper()

# Cleaning expiry date column
df_medical_stock['Expiry_Date'] = pd.to_datetime(df_medical_stock['Expiry_Date'], format = 'mixed').dt.strftime('%Y-%m-%d')

# Cleaning manufacture date column
df_medical_stock['Manufacture_Date'] = pd.to_datetime(df_medical_stock['Manufacture_Date'], format = 'mixed').dt.strftime('%Y-%m-%d')

df_medical_stock['Batch_Number'] = df_medical_stock['Batch_Number'].str.strip().str.upper()

df_medical_stock.head(5)

# ====================================================================
# NOTEBOOK CELL 20
# ====================================================================
# Cleaned medical tests file
df_medical_tests = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_medical_tests.xlsx')

# ====================================================================
# NOTEBOOK CELL 21
# ====================================================================
# Standardizing columns
df_medical_tests.columns = df_medical_tests.columns.str.strip().str.title()

# Cleaning Test Id column
df_medical_tests['Test_Id'] = df_medical_tests['Test_Id'].str.strip().str.upper()

# Cleaning Test Name
df_medical_tests['Test_Name'] = df_medical_tests['Test_Name'].str.strip().str.title()

# Cleaning Category
df_medical_tests['Category'] = df_medical_tests['Category'].str.strip().str.capitalize()

# Cleaning department id
df_medical_tests['Department_Id'] = df_medical_tests['Department_Id'].str.strip().str.upper()

# Cleaning Fasting Required
df_medical_tests['Fasting_Required'] = df_medical_tests['Fasting_Required'].str.strip().str.capitalize()

df_medical_tests.head(5)

# ====================================================================
# NOTEBOOK CELL 22
# ====================================================================
# Cleaning patient medicine data
df_patient_medicine = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_medicine_patient.xlsx')

# Standardizing columns
df_patient_medicine.columns = df_patient_medicine.columns.str.strip().str.title()

# Cleaning Patient_Id column
df_patient_medicine['Patient_Id'] = df_patient_medicine['Patient_Id'].str.strip().str.upper()

# Cleaning medicine_Id column
df_patient_medicine['Medicine_Id'] = df_patient_medicine['Medicine_Id'].str.strip().str.upper()

# Cleaning dispensed date column
df_patient_medicine['Dispensed_Date'] = pd.to_datetime(df_patient_medicine['Dispensed_Date'],format = 'mixed').dt.strftime('%Y-%m-%d')

df_patient_medicine.head(5)

# ====================================================================
# NOTEBOOK CELL 23
# ====================================================================
# Uncleanded patient data
df_patient_data = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_patient.xlsx')

# ====================================================================
# NOTEBOOK CELL 24
# ====================================================================
# Standardize columns data
df_patient_data.columns = df_patient_data.columns.str.strip().str.title()

# Cleaning Patient_Id column
df_patient_data['Patient_Id'] = df_patient_data['Patient_Id'].str.strip().str.upper()

# Cleaning Patient Name column
df_patient_data['Patient_Name'] = df_patient_data['Patient_Name'].str.strip().str.title()

# Cleaning gender column
df_patient_data['Gender'] = df_patient_data['Gender'].str.strip().str.capitalize()

# Cleaning Blood Group column
df_patient_data['Blood_Group'] = df_patient_data['Blood_Group'].str.strip().str.upper()

# Cleaning address column
df_patient_data['Address'] = df_patient_data['Address'].str.strip().str.title()

# Cleaning State column
df_patient_data['State'] = df_patient_data['State'].str.strip().str.capitalize()

# Email address
df_patient_data['Email_Address'] = df_patient_data['Email_Address'].str.strip().str.lower()

# Cleaning status column
df_patient_data['Status'] = df_patient_data['Status'].str.strip().str.capitalize()

# Cleaning admission date column
df_patient_data['Admission_Date'] = pd.to_datetime(df_patient_data['Admission_Date'],format = 'mixed').dt.strftime('%Y-%m-%d')

# Clening discharge date column
df_patient_data['Discharge_Date'] = pd.to_datetime(df_patient_data['Discharge_Date'],format = 'mixed').dt.strftime('%Y-%m-%d')

df_patient_data.head(5)

# ====================================================================
# NOTEBOOK CELL 25
# ====================================================================
# Cleaning patient tests data
df_patients_tests = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_patient_tests.xlsx')

# Cleaning Columns
df_patients_tests.columns = df_patients_tests.columns.str.strip().str.title()

# Cleaning Patient test_id column
df_patients_tests['Patient_Test_Id'] = df_patients_tests['Patient_Test_Id'].str.strip().str.upper()

# Cleaning Patient Id column
df_patients_tests['Patient_Id'] = df_patients_tests['Patient_Id'].str.strip().str.upper()

# Cleaning test_id column
df_patients_tests['Test_Id'] = df_patients_tests['Test_Id'].str.strip().str.upper()

# Cleaning Doctor_Id column
df_patients_tests['Doctor_Id'] = df_patients_tests['Doctor_Id'].str.strip().str.upper()

# Cleaning Test date
df_patients_tests['Test_Date'] = pd.to_datetime(df_patients_tests['Test_Date'],format = 'mixed').dt.strftime('%Y-%m-%d')

# Cleaning result date
df_patients_tests['Result_Date'] = pd.to_datetime(df_patients_tests['Result_Date'],format = 'mixed').dt.strftime('%Y-%m-%d')

# Cleaning Status column
df_patients_tests['Status'] = df_patients_tests['Status'].str.strip().str.capitalize()

# Cleaning Result column
df_patients_tests['Result'] = df_patients_tests['Result'].str.strip().str.capitalize()

# Cleaning Clinical_Notes column
df_patients_tests['Clinical_Notes'] = df_patients_tests['Clinical_Notes'].str.strip().str.capitalize()

# Cleaning Payment_Method column
df_patients_tests['Payment_Method'] = df_patients_tests['Payment_Method'].str.strip().str.title()

# Filling null in discount with 0
df_patients_tests['Discount'] = df_patients_tests['Discount'].fillna(0).astype(int)

df_patients_tests.tail(5)

# ====================================================================
# NOTEBOOK CELL 26
# ====================================================================
# Cleaning rooms data
df_rooms = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_rooms.xlsx')

# Cleaning columns
df_rooms.columns = df_rooms.columns.str.strip().str.title()

# Cleaning room id
df_rooms['Room_Id'] = df_rooms['Room_Id'].str.strip().str.upper()

# Cleaning Department_Id
df_rooms['Department_Id'] = df_rooms['Department_Id'].str.strip().str.upper()

# Cleaning Room_Type
df_rooms['Room_Type'] = df_rooms['Room_Type'].str.strip().str.capitalize()
df_rooms['Room_Type'] = df_rooms['Room_Type'].replace('Icu','ICU')

# Cleaning Status
df_rooms['Status'] = df_rooms['Status'].str.strip().str.capitalize()

df_rooms.head(10)

# ====================================================================
# NOTEBOOK CELL 27
# ====================================================================
# Cleaning satisfaction score data
df_sat_score = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_satisfaction_score.xlsx')

# Standardizing columns
df_sat_score.columns = df_sat_score.columns.str.strip().str.title()

# Cleaning satisfaction id
df_sat_score['Satisfaction_Id'] = df_sat_score['Satisfaction_Id'].str.strip().str.upper()

# Cleaning patient id
df_sat_score['Patient_Id'] = df_sat_score['Patient_Id'].str.strip().str.upper()

# Cleaning doctor id
df_sat_score['Doctor_Id'] = df_sat_score['Doctor_Id'].str.strip().str.upper()

# Cleaning doctor id
df_sat_score['Feedback'] = df_sat_score['Feedback'].str.strip().str.capitalize()

# Cleaning survey date
df_sat_score['Survey_Date'] = pd.to_datetime(df_sat_score['Survey_Date'],format = 'mixed').dt.strftime('%Y-%m-%d')

# Cleaning doctor id
df_sat_score['Department'] = df_sat_score['Department'].str.strip().str.title()

df_sat_score.head(10)

# ====================================================================
# NOTEBOOK CELL 28
# ====================================================================
# Cleaning staff data
df_staff = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_staff.xlsx')

# Standardizing Columns
df_staff.columns = df_staff.columns.str.strip().str.title()

# Cleaning Staff_Id column
df_staff['Staff_Id'] = df_staff['Staff_Id'].str.strip().str.upper()

# Cleaning staff name
df_staff['Staff_Name'] = df_staff['Staff_Name'].str.strip().str.capitalize()

# Cleaning Department_Id
df_staff['Department_Id'] = df_staff['Department_Id'].str.strip().str.upper()

# Cleaning staff name
df_staff['Role'] = df_staff['Role'].str.strip().str.title()

# Cleaning Joining date column
df_staff['Joining_Date'] = pd.to_datetime(df_staff['Joining_Date'],format = 'mixed').dt.strftime('%Y-%m-%d')

# Cleaning Shift
df_staff['Shift'] = df_staff['Shift'].str.strip().str.capitalize()

# Cleaning email address
df_staff['Email_Address'] = df_staff['Email_Address'].str.strip().str.lower()


# Cleaning address column
df_staff['Address'] = df_staff['Address'].map(str) + ' ' + df_staff['Unnamed: 10'].map(str) + ' ' + df_staff['Unnamed: 11']
df_staff['Address'] = df_staff['Address'].str.strip().str.capitalize()
df_staff.drop(columns = ['Unnamed: 10','Unnamed: 11'],inplace = True)

df_staff.head(5)

# ====================================================================
# NOTEBOOK CELL 29
# ====================================================================
# Cleaning supplier data
df_supplier = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_supplier.xlsx')

# Standardizing columns
df_supplier.columns = df_supplier.columns.str.strip().str.title()

# Cleaning supplier id column
df_supplier['Supplier_Id'] = df_supplier['Supplier_Id'].str.strip().str.upper()

# Cleaning Supplier_Name
df_supplier['Supplier_Name'] = df_supplier['Supplier_Name'].str.strip().str.title()

# Cleaning contact person
df_supplier['Contact_Person'] = df_supplier['Contact_Person'].str.strip().str.title()

# Cleaning Email_Address
df_supplier['Email_Address'] = df_supplier['Email_Address'].str.strip().str.lower()

# Cleaning the address column
df_supplier['Address'] = df_supplier['Address'].map(str) +' ' + df_supplier['City'].map(str) + ' ' + df_supplier['State']
df_supplier['Address'] = df_supplier['Address'].str.strip().str.capitalize()
df_supplier.drop(columns = ['City','State'],inplace=True)
df_supplier.rename(columns = {'State.1':'State'},inplace = True)

# Cleaning the state column
df_supplier['State'] = df_supplier['State'].str.strip().str.title()

# Cleaning Start Date and end date column
df_supplier['Contract_Start_Date'] = pd.to_datetime(df_supplier['Contract_Start_Date'],format = 'mixed').dt.strftime('%Y-%m-%d')

# Cleaning Start Date and end date column
df_supplier['Contract_End_Date'] = pd.to_datetime(df_supplier['Contract_End_Date'],format = 'mixed').dt.strftime('%Y-%m-%d')

df_supplier.head(10)

# ====================================================================
# NOTEBOOK CELL 30
# ====================================================================
# Adding Cities to supplier basis state
state_city_map = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubballi", "Mangaluru"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam", "Ramagundam", "Siddipet"]
}

def get_random_city(state):
  cities = state_city_map.get(state, ["Other"])
  return np.random.choice(cities)

df_supplier['City'] = df_supplier['State'].apply(get_random_city)
df_supplier.head(10)

# ====================================================================
# NOTEBOOK CELL 31
# ====================================================================
# Cleaning surgey dataset
df_surgery_data = pd.read_excel('/content/sample_data/Uncleaned_Data/uncleaned_surgery.xlsx')

# ====================================================================
# NOTEBOOK CELL 32
# ====================================================================
# Standardizing column names
df_surgery_data.columns = df_surgery_data.columns.str.strip().str.title()

# Cleaning Appoint id column
df_surgery_data['Appointment_Id'] = df_surgery_data['Appointment_Id'].str.strip().str.upper()

# Cleaning patient Id
df_surgery_data['Patient_Id'] = df_surgery_data['Patient_Id'].str.strip().str.upper()

# Cleaning Doctor_Id column
df_surgery_data['Doctor_Id'] = df_surgery_data['Doctor_Id'].str.strip().str.upper()

# Cleaning Clinical Notes column
df_surgery_data['Clinical_Notes'] = (df_surgery_data['Clinical_Notes'].map(str)+' '+df_surgery_data['Fees']).str.strip().str.capitalize()

# ====================================================================
# NOTEBOOK CELL 33
# ====================================================================
# Cleaning Appointment_Date
df_surgery_data['Appointment_Date'] = df_surgery_data['Appointment_Date'].str.strip()
df_surgery_data['Appointment_Date'] = pd.to_datetime(df_surgery_data['Appointment_Date'],format = 'mixed').dt.strftime('%Y-%m-%d')

# Cleaning Appointment_Time
df_surgery_data['Appointment_Time'] = pd.to_datetime(df_surgery_data['Appointment_Time']).dt.strftime('%H:%M:%S')

# Cleaning Reason column
df_surgery_data['Reason'] = df_surgery_data['Reason'].str.strip().str.title()

# Cleaning Status column
df_surgery_data['Status'] = df_surgery_data['Status'].str.strip().str.capitalize()

# Cleaning fees column
df_surgery_data['Fees'] = np.nan
df_surgery_data['Fees'] = df_surgery_data['Payment_Method'].astype(int)

# Cleaning payment method column
df_surgery_data['Payment_Method'] = df_surgery_data['Discount']
df_surgery_data['Payment_Method'] = df_surgery_data['Payment_Method'].str.strip().str.title()

# Cleaning discount column
df_surgery_data['Discount'] = df_surgery_data['Unnamed: 11'].astype(int)
df_surgery_data.drop(columns = 'Unnamed: 11', inplace = True)

df_surgery_data.head(10)

# ====================================================================
# NOTEBOOK CELL 34
# ====================================================================
# Exporting final datasets

df_appointment.to_excel('./appointments.xlsx',index = False)
df_bed.to_excel('./beds.xlsx',index = False)
df_department.to_excel('./departments.xlsx',index = False)
df_doctors.to_excel('./doctors.xlsx', index = False)
df_bills.to_excel('./hospital_bills.xlsx', index = False)
df_medical_stock.to_excel('./medical_stock.xlsx',index = False)
df_medical_tests.to_excel('./medical_tests.xlsx',index = False)
df_patient_medicine.to_excel('./patient_medicine.xlsx',index = False)
df_patient_data.to_excel('./patient.xlsx', index = False)
df_patients_tests.to_excel('./patient_tests.xlsx', index = False)
df_rooms.to_excel('./rooms.xlsx', index = False)
df_staff.to_excel('./staff.xlsx', index = False)
df_sat_score.to_excel('./satisfaction_score.xlsx', index = False)
df_supplier.to_excel('./supplier.xlsx', index = False)
df_surgery_data.to_excel('./surgery.xlsx', index = False)

# ====================================================================
# NOTEBOOK CELL 35
# ====================================================================
df_staff.to_excel('./staff.xlsx', index = False)
df_sat_score.to_excel('./satisfaction_score.xlsx', index = False)
