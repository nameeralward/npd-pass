document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.carousel-container');
    const slides = document.querySelector('.carousel-slides');
    const prevButton = document.querySelector('.carousel-button.prev');
    const nextButton = document.querySelector('.carousel-button.next');
    const dotsContainer = document.querySelector('.carousel-dots');
    
    let currentSlide = 0;
    const totalSlides = document.querySelectorAll('.carousel-slide').length;

    // Create dots
    for (let i = 0; i < totalSlides; i++) {
        const dot = document.createElement('div');
        dot.classList.add('carousel-dot');
        if (i === 0) dot.classList.add('active');
        dot.addEventListener('click', () => goToSlide(i));
        dotsContainer.appendChild(dot);
    }

    function updateSlidePosition() {
        // Calculate position to center the active slide
        // Add 33.333 to offset the initial transform and center the active slide
        const position = -(currentSlide * 33.333) + 33.333;
        slides.style.transform = `translateX(${position}%)`;
        
        // Update active states for slides and dots
        document.querySelectorAll('.carousel-slide').forEach((slide, index) => {
            slide.classList.toggle('active', index === currentSlide);
        });
        document.querySelectorAll('.carousel-dot').forEach((dot, index) => {
            dot.classList.toggle('active', index === currentSlide);
        });
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        updateSlidePosition();
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
        updateSlidePosition();
    }

    function goToSlide(index) {
        currentSlide = index;
        updateSlidePosition();
    }

    prevButton.addEventListener('click', prevSlide);
    nextButton.addEventListener('click', nextSlide);

    // Start carousel immediately
    updateSlidePosition();
    
    // Pause auto-advance when user interacts with controls
    let autoAdvance = setInterval(nextSlide, 5000);
    
    const resetAutoAdvance = () => {
        clearInterval(autoAdvance);
        autoAdvance = setInterval(nextSlide, 5000);
    };

    // Reset timer when user interacts
    prevButton.addEventListener('click', resetAutoAdvance);
    nextButton.addEventListener('click', resetAutoAdvance);
    dotsContainer.addEventListener('click', resetAutoAdvance);
}); 