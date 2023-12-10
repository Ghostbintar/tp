const slider = document.querySelector('.slider');
const sliderWrapper = document.querySelector('.slider-wrapper');
const slides = document.querySelectorAll('.slide');
const prevArrow = document.querySelector('.arrow.prev');
const nextArrow = document.querySelector('.arrow.next');

let currentIndex = 0;
const slideWidth = slides[0].clientWidth;

function goToSlide(index) {
    sliderWrapper.style.transform = `translateX(-${index * slideWidth}px)`;
    currentIndex = index;
}

prevArrow.addEventListener('click', () => {
    if (currentIndex > 0) {
        goToSlide(currentIndex - 1);
    }
});

nextArrow.addEventListener('click', () => {
    if (currentIndex < slides.length - 1) {
        goToSlide(currentIndex + 1);
    }
});

slides.forEach((slide, index) => {
    slide.addEventListener('click', () => {
        window.location.href = slide.querySelector('.slide-link').href;
    });
});


