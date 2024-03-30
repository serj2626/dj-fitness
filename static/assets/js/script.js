const parent = document.querySelector('.parent')
const addReview = (name, id) => {

    document.getElementById('contactParent').value = id
    document.getElementById('contactComment').innerText = `${name}, `
};



const one = document.querySelector('#one')
const two = document.querySelector('#two')
const three = document.querySelector('#three')
const four = document.querySelector('#four')
const five = document.querySelector('#five')

const stars = [one, two, three, four, five]

const form = document.querySelector('.rate-form');

let hidden = document.getElementById('rateID')


const handleSelect = (index) => {
    stars.slice(0, index + 1).forEach((item) => item.classList.toggle('checked'))
}

stars.forEach((item, index) => item.addEventListener('mouseover', () => {
    handleSelect(index)
}));


stars.forEach((item, index) => item.addEventListener('mouseout', () => {
    handleSelect(index)
}));


stars.forEach((item, index) => item.addEventListener('click', () => {
    console.log('index =>', `${index + 1}`);
    hidden.value = `${index + 1}`;
    console.log('hidden =>', hidden.value);
    console.log('form =>', form);
}));


