let slideIndex = 1;

const showSlides = function showSlidesOfTheCurrentSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].classList.remove('active');
    }
    
    slides[slideIndex - 1].classList.add('active');
}

showSlides(slideIndex);

// Next/previous controls
const plusSlides = function plusSlidesOrMinusSlidesOnClicks(n) {
    showSlides(slideIndex += n);
}


document.querySelector(".prev").addEventListener('click', () => {
    plusSlides(-1);
});

document.querySelector(".next").addEventListener('click', () => {
    plusSlides(1);
});
