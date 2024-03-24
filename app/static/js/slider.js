// slider.js

document.addEventListener("DOMContentLoaded", function() {
    let currentSlide = 0;
    const slides = document.querySelectorAll(".slider-image");
    const totalSlides = slides.length;
    const nextButton = document.querySelector(".slider-btn.next");
    const prevButton = document.querySelector(".slider-btn.prev");
    let slideInterval;

    function updateSlidePosition() {
        slides.forEach((slide, index) => {
            slide.style.transform = `translateX(${(index - currentSlide) * 100}%)`;
        });
    }
    

    function moveToNextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        updateSlidePosition();
    }

    function moveToPrevSlide() {
        currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
        updateSlidePosition();
    }

    function startSlider() {
        slideInterval = setInterval(moveToNextSlide, 3000);
    }

    function pauseSlider() {
        clearInterval(slideInterval);
    }

    nextButton.addEventListener("click", function() {
        moveToNextSlide();
        pauseSlider();
        startSlider();
    });

    prevButton.addEventListener("click", function() {
        moveToPrevSlide();
        pauseSlider();
        startSlider();
    });

    updateSlidePosition();
    startSlider();
});
