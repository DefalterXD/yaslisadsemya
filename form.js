let targetLang;
let defaultLang;

const form = document.querySelector('#showForm');
const formBtnRU = document.querySelector('.form__btn[lang="RU"]');
const formBtnKZ = document.querySelector('.form__btn[lang="KZ"]');
const formSubmitRU = document.querySelector('#showForm button[lang="RU"]');
const formSubmitKZ = document.querySelector('#showForm button[lang="KZ"]');


const switchLanguage = function switchLanguageForForm() {
    const targetList = [...form.querySelectorAll(`*[lang="${targetLang}"]`)];
    const defaultList = [...form.querySelectorAll(`*[lang="${defaultLang}"]`)];
    targetList.map((element) => element.style.display = 'none');
    defaultList.map((element) => element.style.display = 'block');
    form.showModal();
}

window.addEventListener('DOMContentLoaded', () => {
    defaultLang = (document.querySelector('input#switch').checked) ? 'KZ' : 'RU';
    targetLang = (document.querySelector('input#switch').checked) ? 'RU' : 'KZ';
});

document.querySelector('input#switch').addEventListener('input', (event) => {
    targetLang = (event.target.checked) ? 'RU' : 'KZ';
    defaultLang = (event.target.checked) ? 'KZ' : 'RU';
    
});

form.querySelector('.close').addEventListener('click', () => {
    form.close();
});

formBtnRU.addEventListener('click', () => {
    switchLanguage();
});

formBtnKZ.addEventListener('click', () => {
    switchLanguage();
});

formSubmitRU.addEventListener('click', (e) => {
    e.preventDefault();
});

formSubmitKZ.addEventListener('click', (e) => {
    e.preventDefault();
});