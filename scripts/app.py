import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Standalone generators
from generators.appointment_generator import generate_appointments
from generators.bed_generator import generate_beds
from generators.bill_generator import generate_bills
from generators.department_generator import generate_departments
from generators.doctor_generator import generate_doctors
from generators.medical_stock_generator import generate_medical_stock
from generators.medical_tests_generator import generate_medical_tests
from generators.medicine_patient_generator import generate_medicine_patient
from generators.patient_generator import generate_patients
from generators.patient_tests_generator import generate_patient_tests
from generators.room_generator import generate_rooms
from generators.satisfaction_score_generator import generate_satisfaction_scores
from generators.staff_generator import generate_staff
from generators.supplier_generator import generate_suppliers
from generators.surgery_generator import generate_surgeries


class ModernHospitalGeneratorUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Analytics • Data Studio")
        self.root.geometry("940x1000")
        self.root.configure(bg="#0F172A")
        self.root.resizable(False, False)

        # Output directory default
        self.target_dir = tk.StringVar(
            value=os.path.abspath("./hospital_raw_data")
        )

        # Datasets registry
        self.datasets = [
            {
                "key": "patients",
                "label": "Patient Demographics",
                "file": "uncleaned_patient.xlsx",
                "desc": "Demographics, vitals, admissions & status",
                "func": generate_patients,
            },
            {
                "key": "appointments",
                "label": "Appointments",
                "file": "uncleaned_appointments.xlsx",
                "desc": "Clinical admissions, diagnoses & doctor reviews",
                "func": generate_appointments,
            },
            {
                "key": "surgeries",
                "label": "Surgeries & Consultations",
                "file": "uncleaned_surgery.xlsx",
                "desc": "Surgical reviews, fees & column-shifted records",
                "func": generate_surgeries,
            },
            {
                "key": "rooms",
                "label": "Hospital Rooms",
                "file": "uncleaned_rooms.xlsx",
                "desc": "Room types, department floors, rates & capacity",
                "func": generate_rooms,
            },
            {
                "key": "beds",
                "label": "Bed & Room Allocations",
                "file": "uncleaned_beds.xlsx",
                "desc": "Wards, occupancy tracking & patient stays",
                "func": generate_beds,
            },
            {
                "key": "departments",
                "label": "Hospital Departments",
                "file": "uncleaned_departments.xlsx",
                "desc": "Staffing counts, head doctors & floor plans",
                "func": generate_departments,
            },
            {
                "key": "doctors",
                "label": "Doctor Directory",
                "file": "uncleaned_doctors.xlsx",
                "desc": "Specializations, salaries, experience & profiles",
                "func": generate_doctors,
            },
            {
                "key": "staff",
                "label": "Hospital Staff & Nurses",
                "file": "uncleaned_staff.xlsx",
                "desc": "Nursing staff, ward boys, shifts & salaries",
                "func": generate_staff,
            },
            {
                "key": "bills",
                "label": "Hospital Billing",
                "file": "uncleaned_hospital_bills.xlsx",
                "desc": "Room rates, surgeries, medicines & payments",
                "func": generate_bills,
            },
            {
                "key": "stock",
                "label": "Medical Pharmacy Stock",
                "file": "uncleaned_medical_stock.xlsx",
                "desc": "Batch numbers, reorder thresholds & prices",
                "func": generate_medical_stock,
            },
            {
                "key": "suppliers",
                "label": "Pharmaceutical Suppliers",
                "file": "uncleaned_supplier.xlsx",
                "desc": "Vendor contacts, pincodes & contract dates",
                "func": generate_suppliers,
            },
            {
                "key": "tests",
                "label": "Diagnostic Medical Tests",
                "file": "uncleaned_medical_tests.xlsx",
                "desc": "Master catalog of tests, costs & departments",
                "func": generate_medical_tests,
            },
            {
                "key": "patient_tests",
                "label": "Patient Diagnostic Orders",
                "file": "uncleaned_patient_tests.xlsx",
                "desc": "Ordered lab tests, findings, results & billing",
                "func": generate_patient_tests,
            },
            {
                "key": "med_patient",
                "label": "Patient Medication Dispenses",
                "file": "uncleaned_medicine_patient.xlsx",
                "desc": "Dispensed prescription logs & dosages",
                "func": generate_medicine_patient,
            },
            {
                "key": "satisfaction",
                "label": "Patient Satisfaction Scores",
                "file": "uncleaned_satisfaction_score.xlsx",
                "desc": "Doctor evaluations, ratings & feedback reviews",
                "func": generate_satisfaction_scores,
            },
        ]

        self.btn_widgets = {}
        self.badge_widgets = {}
        self.build_ui()

    def build_ui(self):
        # 1. Header Banner
        header = tk.Frame(self.root, bg="#1E293B", height=78)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_box = tk.Frame(header, bg="#1E293B")
        title_box.pack(side="left", padx=24, pady=10)

        tk.Label(
            title_box,
            text="🏥 Hospital Synthetic Data Studio",
            font=("Segoe UI", 15, "bold"),
            fg="#F8FAFC",
            bg="#1E293B",
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="Automated generation with deliberate formatting inconsistencies for cleaning practice",
            font=("Segoe UI", 8),
            fg="#94A3B8",
            bg="#1E293B",
        ).pack(anchor="w", pady=(1, 0))

        # 2. Destination Directory Card
        dest_card = tk.Frame(
            self.root,
            bg="#1E293B",
            bd=0,
            highlightbackground="#334155",
            highlightthickness=1,
        )
        dest_card.pack(fill="x", padx=24, pady=(10, 6))

        tk.Label(
            dest_card,
            text="STORAGE DESTINATION",
            font=("Segoe UI", 8, "bold"),
            fg="#38BDF8",
            bg="#1E293B",
        ).pack(anchor="w", padx=14, pady=(6, 2))

        entry_box = tk.Frame(dest_card, bg="#1E293B")
        entry_box.pack(fill="x", padx=14, pady=(0, 8))

        self.entry_dir = tk.Entry(
            entry_box,
            textvariable=self.target_dir,
            font=("Consolas", 10),
            bg="#0F172A",
            fg="#E2E8F0",
            insertbackground="#38BDF8",
            relief="flat",
            bd=6,
            state="readonly",
        )
        self.entry_dir.pack(side="left", fill="x", expand=True, padx=(0, 10))

        tk.Button(
            entry_box,
            text="Change Folder",
            font=("Segoe UI", 9, "bold"),
            bg="#334155",
            fg="#F8FAFC",
            activebackground="#475569",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=4,
            command=self.browse_folder,
        ).pack(side="right")

        # 3. Datasets Queue Card
        queue_card = tk.Frame(
            self.root,
            bg="#1E293B",
            highlightbackground="#334155",
            highlightthickness=1,
        )
        queue_card.pack(fill="both", expand=True, padx=24, pady=(0, 8))

        queue_header = tk.Frame(queue_card, bg="#1E293B")
        queue_header.pack(fill="x", padx=14, pady=(6, 2))

        tk.Label(
            queue_header,
            text=f"DATASETS REPOSITORY ({len(self.datasets)} TABLES)",
            font=("Segoe UI", 8, "bold"),
            fg="#94A3B8",
            bg="#1E293B",
        ).pack(side="left")

        # Dataset Rows
        for item in self.datasets:
            row = tk.Frame(queue_card, bg="#1E293B", pady=1)
            row.pack(fill="x", padx=14, pady=1)

            meta = tk.Frame(row, bg="#1E293B")
            meta.pack(side="left", fill="x", expand=True)

            tk.Label(
                meta,
                text=item["label"],
                font=("Segoe UI", 9, "bold"),
                fg="#F1F5F9",
                bg="#1E293B",
            ).pack(anchor="w")

            tk.Label(
                meta,
                text=f"{item['desc']} • {item['file']}",
                font=("Segoe UI", 7),
                fg="#64748B",
                bg="#1E293B",
            ).pack(anchor="w")

            badge = tk.Label(
                row,
                text="PENDING",
                font=("Segoe UI", 7, "bold"),
                fg="#94A3B8",
                bg="#0F172A",
                padx=8,
                pady=1,
            )
            badge.pack(side="left", padx=10)
            self.badge_widgets[item["key"]] = badge

            btn = tk.Button(
                row,
                text="Generate",
                font=("Segoe UI", 8, "bold"),
                bg="#2563EB",
                fg="#FFFFFF",
                activebackground="#1D4ED8",
                activeforeground="#FFFFFF",
                relief="flat",
                cursor="hand2",
                width=16,
                pady=1,
                command=lambda ds=item: self.run_single_generation(ds),
            )
            btn.pack(side="right")
            self.btn_widgets[item["key"]] = btn

        # 4. Action Bar
        bottom_frame = tk.Frame(self.root, bg="#0F172A")
        bottom_frame.pack(fill="x", padx=24, pady=(0, 10))

        tk.Button(
            bottom_frame,
            text=f"⚡ Generate All {len(self.datasets)} Datasets Concurrently",
            font=("Segoe UI", 11, "bold"),
            bg="#0284C7",
            fg="#FFFFFF",
            activebackground="#0369A1",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            pady=7,
            command=self.run_all_generation,
        ).pack(fill="x")

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.target_dir.get())
        if folder:
            folder = os.path.normpath(folder)
            self.target_dir.set(folder)

            # Update entry display
            self.entry_dir.config(state="normal")
            self.entry_dir.delete(0, tk.END)
            self.entry_dir.insert(0, folder)
            self.entry_dir.config(state="readonly")

    def mark_button_success(self, ds_key):
        btn = self.btn_widgets[ds_key]
        badge = self.badge_widgets[ds_key]

        btn.config(
            text="✔ Successfully Created",
            bg="#16A34A",
            fg="#FFFFFF",
            activebackground="#15803D",
            activeforeground="#FFFFFF",
        )
        badge.config(
            text="READY",
            fg="#4ADE80",
            bg="#064E3B",
        )

    def run_single_generation(self, dataset_item):
        target_folder = self.target_dir.get()
        os.makedirs(target_folder, exist_ok=True)
        filepath = os.path.join(target_folder, dataset_item["file"])

        try:
            dataset_item["func"](filepath)
            self.mark_button_success(dataset_item["key"])
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed generating {dataset_item['file']}:\n{e}"
            )

    def run_all_generation(self):
        target_folder = self.target_dir.get()
        os.makedirs(target_folder, exist_ok=True)

        for ds in self.datasets:
            filepath = os.path.join(target_folder, ds["file"])
            ds["func"](filepath)
            self.mark_button_success(ds["key"])

        messagebox.showinfo(
            "Pipeline Complete",
            f"All {len(self.datasets)} hospital datasets generated in:\n{target_folder}",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernHospitalGeneratorUI(root)
    root.mainloop()