const imgRow = document.querySelector('.row');
const expandImg = document.querySelector('.expanded__container img');

const choosedTargetImg = function choosedTargetImgFromImgRow(img) {
    expandImg.classList.remove('animate');
    
    void expandImg.offsetWidth; 
    
    expandImg.src = img.src;
    expandImg.alt = img.alt;
    
    expandImg.classList.add('animate');
}

imgRow.addEventListener('click', (e) => {
    if (e.target.tagName === 'IMG') {
        choosedTargetImg(e.target);
    }
});