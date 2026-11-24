
document.addEventListener("DOMContentLoaded", () => {

    // Python scripts grouped by category
    const scripts = {
        generation: [
            {
                name: "appointment_generator.py",
                path: "scripts/appointment_generator.py",
                description: "Generates synthetic hospital appointment records."
            },
            {
                name: "bed_generator.py",
                path: "scripts/bed_generator.py",
                description: "Generates hospital bed records."
            },
            {
                name: "bill_generator.py",
                path: "scripts/bill_generator.py",
                description: "Generates patient billing records."
            },
            {
                name: "department_generator.py",
                path: "scripts/department_generator.py",
                description: "Generates hospital department records."
            },
            {
                name: "doctor_generator.py",
                path: "scripts/doctor_generator.py",
                description: "Generates doctor records."
            },
            {
                name: "medical_stock_generator.py",
                path: "scripts/medical_stock_generator.py",
                description: "Generates medical stock records."
            },
            {
                name: "medical_tests_generator.py",
                path: "scripts/medical_tests_generator.py",
                description: "Generates medical test records."
            },
            {
                name: "medicine_patient_generator.py",
                path: "scripts/medicine_patient_generator.py",
                description: "Generates patient medicine records."
            },
            {
                name: "patient_generator.py",
                path: "scripts/patient_generator.py",
                description: "Generates patient records."
            },
            {
                name: "patient_sync.py",
                path: "scripts/patient_sync.py",
                description: "Synchronizes patient records."
            },
            {
                name: "patient_tests_generator.py",
                path: "scripts/patient_tests_generator.py",
                description: "Generates patient test records."
            },
            {
                name: "room_generator.py",
                path: "scripts/room_generator.py",
                description: "Generates hospital room records."
            },
            {
                name: "satisfaction_score_generator.py",
                path: "scripts/satisfaction_score_generator.py",
                description: "Generates patient satisfaction scores."
            },
            {
                name: "staff_generator.py",
                path: "scripts/staff_generator.py",
                description: "Generates hospital staff records."
            },
            {
                name: "supplier_generator.py",
                path: "scripts/supplier_generator.py",
                description: "Generates supplier records."
            },
            {
                name: "surgery_generator.py",
                path: "scripts/surgery_generator.py",
                description: "Generates surgery records."
            },
            {
                name: "application_interface.py",
                path: "scripts/app.py",
                description: "A tkinter interface to generate record files"
            },
            {
                name: "data_inserter_sql.py",
                path: "scripts/data_inserter_sql.py",
                description: "Inserts clean data into SQL DB"
            }
        ],

        cleaning: [
            // Add your actual cleaning scripts here.
            // Example:
            {
                 name: "hospital_data_cleaning.py",
                 path: "scripts/Hospital_Data_Cleaning.py",
                 description: "Cleans and standardizes the entire dataset."
            }
        ]
    };

    // HTML elements
    const fileList = document.getElementById("file-list");
    const folderTitle = document.getElementById("folder-title");
    const activeFilename = document.getElementById("active-filename");
    const scriptDescription = document.getElementById("script-description");
    const codeDisplay = document.getElementById("code-display");
    const copyButton = document.getElementById("copy-code");
    const codeStatus = document.getElementById("code-status");

    const categoryButtons = document.querySelectorAll(".python-category");

    let currentCode = "";

    // Load selected Python file
    async function loadScript(script) {

        activeFilename.textContent = script.name;
        scriptDescription.textContent = script.description;
        codeDisplay.textContent = "# Loading script...";
        currentCode = "";

        copyButton.disabled = true;
        codeStatus.textContent = "Loading...";

        try {
            const response = await fetch(script.path);

            if (!response.ok) {
                throw new Error("Unable to load " + script.name);
            }

            const code = await response.text();

            currentCode = code;
            codeDisplay.textContent = code;

            if (window.Prism) {
                Prism.highlightElement(codeDisplay);
            }

            copyButton.disabled = false;
            codeStatus.textContent = "Loaded successfully";

        } catch (error) {

            codeDisplay.textContent =
                "# Unable to load this script.\n" +
                "# Check the file path and filename.";

            codeStatus.textContent = "Loading failed";

            console.error(error);
        }
    }

    // Display files for selected category
    function displayFiles(category) {

        fileList.innerHTML = "";

        const categoryScripts = scripts[category];

        folderTitle.textContent =
            category === "generation"
                ? "DATA GENERATION"
                : "DATA CLEANING";

        if (!categoryScripts || categoryScripts.length === 0) {

            fileList.textContent = "No scripts added yet.";
            activeFilename.textContent = "No file selected";
            scriptDescription.textContent =
                "Add your cleaning scripts to display them here.";
            codeDisplay.textContent = "# No script selected.";
            currentCode = "";
            copyButton.disabled = true;

            return;
        }

        categoryScripts.forEach((script, index) => {

            const button = document.createElement("button");

            button.className = "file-item";
            button.textContent = "🐍 " + script.name;

            button.addEventListener("click", () => {

                document.querySelectorAll(".file-item")
                    .forEach(item => item.classList.remove("active"));

                button.classList.add("active");

                loadScript(script);
            });

            fileList.appendChild(button);

            // Automatically load the first file
            if (index === 0) {
                button.classList.add("active");
                loadScript(script);
            }
        });
    }

    // Category navigation
    categoryButtons.forEach(button => {

        button.addEventListener("click", () => {

            categoryButtons.forEach(item =>
                item.classList.remove("active")
            );

            button.classList.add("active");

            displayFiles(button.dataset.category);
        });
    });

    // Copy selected code
    copyButton.addEventListener("click", async () => {

        if (!currentCode) return;

        try {
            await navigator.clipboard.writeText(currentCode);

            copyButton.textContent = "Copied!";

            setTimeout(() => {
                copyButton.textContent = "Copy Code";
            }, 1500);

        } catch (error) {
            codeStatus.textContent = "Copy failed";
            console.error(error);
        }
    });

    // Initial display
    displayFiles("generation");

});
