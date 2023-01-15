const cashInput = document.getElementById('cash');
const ctotal = document.getElementById('ctotal');


const choices = document.getElementsByClassName('button-choices');

cashInput.addEventListener('input', (e) => {
    const cashValue = Math.floor(e.target.value);
    ctotal.textContent = `${cashValue.toLocaleString()}`; 
});

for (let i = 0; i < choices.length; i++) {
    choices[i].addEventListener('click', (e) => {
        const cashValue = cashInput.value;
        const interest = e.target.value.split("-")[1].replace("%","")/100;
        const months = e.target.value.split("-")[0].replace(" Meses","");
        const total = Math.floor(cashValue*(1+(interest*months)));
        ctotal.textContent = `${total.toLocaleString()}`;
    });
}