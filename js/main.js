
document.addEventListener("DOMContentLoaded", () => {

    // ==========================================
    // 1. SELECT NAVIGATION BUTTONS AND PANELS
    // ==========================================

    const tabs = document.querySelectorAll(".tech-tab");
    const panels = document.querySelectorAll(".tech-panel");


    // ==========================================
    // 2. NAVIGATION FUNCTION
    // ==========================================

    function activateTab(target) {

        // Check whether the requested panel exists
        const selectedPanel = document.getElementById(target);

        if (!selectedPanel) {
            console.warn("Navigation panel not found:", target);
            return;
        }

        // Remove active class from all navigation buttons
        tabs.forEach(tab => {
            tab.classList.remove("active");
            tab.setAttribute("aria-selected", "false");
        });

        // Hide all technology panels
        panels.forEach(panel => {
            panel.classList.remove("active");
            panel.setAttribute("hidden", "");
        });

        // Activate selected navigation button
        const selectedTab = document.querySelector(
            `.tech-tab[data-target="${target}"]`
        );

        if (selectedTab) {
            selectedTab.classList.add("active");
            selectedTab.setAttribute("aria-selected", "true");
        }

        // Display selected panel
        selectedPanel.classList.add("active");
        selectedPanel.removeAttribute("hidden");

    }


    // ==========================================
    // 3. ADD CLICK EVENTS TO NAVIGATION BUTTONS
    // ==========================================

    tabs.forEach(tab => {

        tab.addEventListener("click", () => {

            const target = tab.dataset.target;

            activateTab(target);

        });

    });


    // ==========================================
    // 4. INITIALIZE DEFAULT TAB
    // ==========================================

    const initialTab = document.querySelector(
        ".tech-tab.active"
    );

    activateTab(
        initialTab ? initialTab.dataset.target : "overview"
    );


});
