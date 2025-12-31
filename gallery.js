window.addEventListener('scroll', () => {
    const header = document.querySelector('.header__container');
    if (window.scrollY > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

const gallery = document.querySelector('.gallery__wrapper');
const imgModal = document.querySelector('#showImage');

const showImage = function showSpecificImageFromGallery(img) {
    const newImg = imgModal.querySelector('img');
    newImg.src = img.src;
    newImg.alt = img.alt;
    
    imgModal.style.display = 'grid';
    imgModal.show();
};

gallery.addEventListener('click', (event) => {
    if (event.target.tagName === 'IMG') showImage(event.target);
});

imgModal.querySelector('.close').addEventListener('click', () => {
    imgModal.style.display = 'none';
    imgModal.close();
});