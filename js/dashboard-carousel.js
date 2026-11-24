
document.addEventListener("DOMContentLoaded", function () {

    // Carousel Elements
    const track = document.getElementById("dashboard-track");
    const carousel = document.querySelector(".dashboard-carousel");

    const previousButton = document.getElementById("dashboard-prev");
    const nextButton = document.getElementById("dashboard-next");

    const indicatorsContainer =
        document.getElementById("dashboard-indicators");

    const pageCounter =
        document.getElementById("dashboard-counter");


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


    // Get All Dashboard Slides
    const slides = Array.from(
        track.querySelectorAll(".dashboard-slide")
    );

    let currentSlide = 0;

    if (slides.length === 0) return;


    // Create Navigation Indicators
    function createIndicators() {

        indicatorsContainer.innerHTML = "";

        slides.forEach((slide, index) => {

            const dot = document.createElement("button");

            dot.type = "button";
            dot.className = "dashboard-carousel-dot";

            dot.setAttribute(
                "aria-label",
                `Go to dashboard ${index + 1}`
            );

            dot.addEventListener("click", function () {
                showSlide(index);
            });

            indicatorsContainer.appendChild(dot);

        });

    }


    // Display Selected Slide
    function showSlide(index) {

        currentSlide = Math.max(
            0,
            Math.min(index, slides.length - 1)
        );


        // Calculate actual slide position
        const firstSlidePosition = slides[0].offsetLeft;

        const selectedSlidePosition =
            slides[currentSlide].offsetLeft;

        const movement =
            selectedSlidePosition - firstSlidePosition;


        // Move Carousel Track
        track.style.transform =
            `translateX(-${movement}px)`;


        // Update Active Indicator
        const dots = indicatorsContainer.querySelectorAll(
            ".dashboard-carousel-dot"
        );

        dots.forEach((dot, dotIndex) => {

            dot.classList.toggle(
                "active",
                dotIndex === currentSlide
            );

        });


        // Update Page Counter
        const current = String(currentSlide + 1).padStart(2, "0");

        const total = String(slides.length).padStart(2, "0");

        pageCounter.textContent = `${current} / ${total}`;


        // Update Navigation Buttons
        previousButton.disabled = currentSlide === 0;

        nextButton.disabled =
            currentSlide === slides.length - 1;

    }


    // Previous Slide
    previousButton.addEventListener("click", function () {

        if (currentSlide > 0) {
            showSlide(currentSlide - 1);
        }

    });


    // Next Slide
    nextButton.addEventListener("click", function () {

        if (currentSlide < slides.length - 1) {
            showSlide(currentSlide + 1);
        }

    });


    // Recalculate Position on Resize
    if ("ResizeObserver" in window) {

        const resizeObserver = new ResizeObserver(function () {
            showSlide(currentSlide);
        });

        resizeObserver.observe(carousel);

    } else {

        window.addEventListener("resize", function () {
            showSlide(currentSlide);
        });

    }


    // Initialize Carousel
    createIndicators();

    showSlide(0);

});
