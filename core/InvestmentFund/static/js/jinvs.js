const cashInput = document.getElementById('cash');
const ctotal = document.getElementById('ctotal');

const rammount = document.getElementById('rammount');
const rinterest = document.getElementById('rinterest');
const rtotal = document.getElementById('rtotal');
const daylint = document.getElementById('daylint');

const choices = document.getElementsByClassName('button-choices');

cashInput.addEventListener('input', (e) => {
    const cashValue = Math.round(e.target.value);
    ctotal.textContent = `${cashValue.toLocaleString()}`; 
});

for (let i = 0; i < choices.length; i++) {
    choices[i].addEventListener('click', (e) => {
        const cashValue = cashInput.value;
        const interest = e.target.value.split("-")[1].replace("%","")/100;
        const months = e.target.value.split("-")[0].replace(" Meses","");
        const total = Math.round(cashValue*(1+(interest*months)));

        const finterest = Math.round(total-cashValue);
        const dayli = Math.round(finterest/(months*30));

        ctotal.textContent = `${total.toLocaleString()}`;
        rammount.textContent = `$ ${cashValue.toLocaleString()}`;
        rinterest.textContent = `$ ${finterest.toLocaleString()}`;
        rtotal.textContent = `$ ${total.toLocaleString()}`;
        daylint.textContent = `$ ${dayli.toLocaleString()}`;
    });
}