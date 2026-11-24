
document.addEventListener("DOMContentLoaded", () => {

    // Database table configuration
    const tables = [
        {
            name: "Patients",
            file: "patient_data.json",
            description: "Patient master data and admission details."
        },
        {
            name: "Doctors",
            file: "doctors_data.json",
            description: "Doctor profiles and professional information."
        },
        {
            name: "Appointments",
            file: "appointments_data.json",
            description: "Hospital appointment records."
        },
        {
            name: "Departments",
            file: "departments_data.json",
            description: "Hospital department information."
        },
        {
            name: "Hospital Bills",
            file: "hospital_bills_data.json",
            description: "Patient billing and payment records."
        },
        {
            name: "Beds",
            file: "beds_data.json",
            description: "Hospital bed allocation and occupancy."
        },
        {
            name: "Rooms",
            file: "rooms_data.json",
            description: "Hospital room information."
        },
        {
            name: "Medical Tests",
            file: "medical_tests_data.json",
            description: "Available medical tests and details."
        },
        {
            name: "Medical Stock",
            file: "medical_stock_data.json",
            description: "Hospital medical stock information."
        },
        {
            name: "Staff",
            file: "staff_data.json",
            description: "Hospital staff information."
        },
        {
            name: "Suppliers",
            file: "supplier_data.json",
            description: "Hospital supplier information."
        },
        {
            name: "Surgeries",
            file: "Surgery_data.json",
            description: "Hospital surgery records."
        },
        {
            name: "Satisfaction Score",
            file: "satisfaction_score_data.json",
            description: "Reviews of patients"
        },
        {
            name:"Patient Test Data",
            file: "patient_tests_data.json",
            description: "Data for different tests done by patients."
        },
        {
            name: "Patient Medicine",
            file: "patient_medicine_data.json",
            description: "Patient Medicine consumption data."
        }
    ];


    // HTML elements
    const tableList = document.getElementById("sql-table-list");
    const tableCount = document.getElementById("sql-table-count");

    const selectedTable = document.getElementById("sql-selected-table");
    const tableDescription = document.getElementById("sql-table-description");

    const sampleCount = document.getElementById("sql-sample-count");

    const tableHead = document.getElementById("sql-table-head");
    const tableBody = document.getElementById("sql-table-body");

    const tableScroll = document.getElementById("sql-table-scroll");

    const loadingMessage = document.getElementById("sql-loading");
    const errorMessage = document.getElementById("sql-error");

    const showingRecords = document.getElementById("sql-showing-records");
    const currentTable = document.getElementById("sql-current-table");
    const totalRecords = document.getElementById("sql-total-records");

    const copyButton = document.getElementById("copy-sql-query");

    let currentQuery = "";


    // Display database table buttons
    function renderTableList() {

        tableList.innerHTML = "";

        tableCount.textContent = `${tables.length} Tables`;

        tables.forEach((table, index) => {

            const button = document.createElement("button");

            button.type = "button";
            button.className = "sql-table-item";
            button.textContent = table.name;

            button.addEventListener("click", () => {

                document.querySelectorAll(".sql-table-item")
                    .forEach(item => item.classList.remove("active"));

                button.classList.add("active");

                loadTable(table);

            });

            tableList.appendChild(button);

            // Automatically load first table
            if (index === 0) {
                button.classList.add("active");
                loadTable(table);
            }

        });

    }


    // Load JSON file
    async function loadTable(table) {

        selectedTable.textContent = table.name;
        tableDescription.textContent = table.description;

        tableHead.innerHTML = "";
        tableBody.innerHTML = "";

        tableScroll.hidden = true;
        errorMessage.hidden = true;
        loadingMessage.hidden = false;

        loadingMessage.textContent = "Loading table records...";

        sampleCount.textContent = "Loading...";
        showingRecords.textContent = "Loading records...";
        currentTable.textContent = `Table: ${table.name}`;
        totalRecords.textContent = "Total Records: —";

        copyButton.disabled = true;
        currentQuery = "";


        try {

            const response = await fetch(`data/${table.file}`);

            if (!response.ok) {
                throw new Error(`Unable to load ${table.file}: HTTP ${response.status}`);
            }

            const data = await response.json();

            if (!Array.isArray(data.columns) || !Array.isArray(data.records)) {
                throw new Error("Invalid JSON structure. Expected columns and records arrays.");
            }

            // Generate SQL query for display/copy
            currentQuery = `SELECT * FROM ${table.name.replace(/\s+/g, "_")} LIMIT 10;`;

            // Render table
            renderTableData(data);

        }

        catch (error) {

            console.error("SQL Explorer Error:", error);

            loadingMessage.hidden = true;
            tableScroll.hidden = true;

            errorMessage.hidden = false;
            errorMessage.textContent =
                `Unable to load ${table.file}. Check that the JSON file exists in the data folder and follows the expected structure.`;

            sampleCount.textContent = "0 sample records";
            showingRecords.textContent = "Unable to display records";
            totalRecords.textContent = "Total Records: —";

        }

    }


    // Render table data
    function renderTableData(data) {

        loadingMessage.hidden = true;
        errorMessage.hidden = true;

        tableHead.innerHTML = "";
        tableBody.innerHTML = "";

        // Create table headings
        const headerRow = document.createElement("tr");

        data.columns.forEach(column => {

            const th = document.createElement("th");

            th.textContent = column;

            headerRow.appendChild(th);

        });

        tableHead.appendChild(headerRow);


        // Display first 10 records
        const records = data.records.slice(0, 10);

        records.forEach(record => {

            const row = document.createElement("tr");

            data.columns.forEach(column => {

                const cell = document.createElement("td");

                const value = record[column];

                if (value === null || value === undefined || value === "") {
                    cell.textContent = "—";
                }

                else if (typeof value === "object") {
                    cell.textContent = JSON.stringify(value);
                }

                else {
                    cell.textContent = String(value);
                }

                row.appendChild(cell);

            });

            tableBody.appendChild(row);

        });


        // Update table information
        tableScroll.hidden = false;

        sampleCount.textContent =
            `${records.length} sample records`;

        showingRecords.textContent =
            `Showing ${records.length} of ${data.total_records.toLocaleString()} records`;

        currentTable.textContent =
            `Table: ${data.table_name || "Selected Table"}`;

        totalRecords.textContent =
            `Total Records: ${data.total_records.toLocaleString()}`;

        copyButton.disabled = false;

    }


    // Copy SQL query
    copyButton.addEventListener("click", async () => {

        if (!currentQuery) return;

        try {

            await navigator.clipboard.writeText(currentQuery);

            copyButton.textContent = "Copied!";

            setTimeout(() => {
                copyButton.textContent = "Copy SQL Query";
            }, 1500);

        }

        catch (error) {

            console.error("Copy failed:", error);
            copyButton.textContent = "Copy failed";

            setTimeout(() => {
                copyButton.textContent = "Copy SQL Query";
            }, 1500);

        }

    });


    // Initialize explorer
    renderTableList();

});
