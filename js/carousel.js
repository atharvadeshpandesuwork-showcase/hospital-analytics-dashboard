
document.addEventListener("DOMContentLoaded", function () {

    // Carousel Elements
    const track = document.getElementById("powerbi-carousel-track");
    const carousel = document.querySelector(".powerbi-carousel");

    const previousButton = document.getElementById("powerbi-prev");
    const nextButton = document.getElementById("powerbi-next");

    const indicatorsContainer =
        document.getElementById("powerbi-indicators");

    const pageCounter =
        document.getElementById("powerbi-page-counter");


    // Validate Elements
    if (
        !track ||
        !carousel ||
        !previousButton ||
        !nextButton ||
        !indicatorsContainer ||
        !pageCounter
    ) {
        return;
    }


    // Get Dashboard Pages
    const pages = Array.from(
        track.querySelectorAll(".powerbi-page")
    );

    let currentPage = 0;

    if (pages.length === 0) return;


    // Create Navigation Indicators
    function createIndicators() {

        indicatorsContainer.innerHTML = "";

        pages.forEach((page, index) => {

            const dot = document.createElement("button");

            dot.type = "button";
            dot.className = "powerbi-carousel-dot";

            dot.setAttribute(
                "aria-label",
                `Go to dashboard page ${index + 1}`
            );

            dot.addEventListener("click", function () {
                showPage(index);
            });

            indicatorsContainer.appendChild(dot);

        });

    }


    // Display Selected Page
    function showPage(index) {

        currentPage = Math.max(
            0,
            Math.min(index, pages.length - 1)
        );


        // Calculate Actual Position of Selected Slide
        const firstSlidePosition = pages[0].offsetLeft;

        const currentSlidePosition =
            pages[currentPage].offsetLeft;

        const movement =
            currentSlidePosition - firstSlidePosition;


        // Move Carousel Track
        track.style.transform =
            `translateX(-${movement}px)`;


        // Update Navigation Indicators
        const dots = indicatorsContainer.querySelectorAll(
            ".powerbi-carousel-dot"
        );

        dots.forEach((dot, dotIndex) => {

            dot.classList.toggle(
                "active",
                dotIndex === currentPage
            );

            dot.setAttribute(
                "aria-current",
                dotIndex === currentPage ? "true" : "false"
            );

        });


        // Update Page Counter
        const current = String(currentPage + 1).padStart(2, "0");

        const total = String(pages.length).padStart(2, "0");

        pageCounter.textContent = `${current} / ${total}`;


        // Update Navigation Buttons
        previousButton.disabled = currentPage === 0;

        nextButton.disabled =
            currentPage === pages.length - 1;

    }


    // Previous Button
    previousButton.addEventListener("click", function () {

        if (currentPage > 0) {
            showPage(currentPage - 1);
        }

    });


    // Next Button
    nextButton.addEventListener("click", function () {

        if (currentPage < pages.length - 1) {
            showPage(currentPage + 1);
        }

    });


    // Recalculate Position on Resize
    if ("ResizeObserver" in window) {

        const resizeObserver = new ResizeObserver(function () {

            showPage(currentPage);

        });

        resizeObserver.observe(carousel);

    } else {

        window.addEventListener("resize", function () {

            showPage(currentPage);

        });

    }


    // Initialize Carousel
    createIndicators();

    showPage(0);

});
