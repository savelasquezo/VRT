const cashInput = document.getElementById('cash');
const intsInput = document.getElementById('pinterest');
const montInput = document.getElementById('pmonths');

const ctotal = document.getElementById('ctotal');
const rammount = document.getElementById('rammount');
const rinterest = document.getElementById('rinterest');
const daylint = document.getElementById('daylint');
const rtotal = document.getElementById('rtotal');


const updateValues = () => {
  const cashValue = Math.round(cashInput.value);
  const intsValue = intsInput.value;
  const montValue = Math.round(montInput.value);
  
  const total = Math.round(cashValue * (1 + (intsValue/100) * montValue));
  const finterest = Math.round(total - cashValue);

  let dayli;
  if (!montValue || montValue === 0) {
    dayli = 0;
  } else {
    dayli = Math.round(finterest/(montValue*30));
  }

  ctotal.textContent = total.toLocaleString();
  rammount.textContent = `$ ${cashValue.toLocaleString()}`;
  rinterest.textContent = `$ ${finterest.toLocaleString()}`;
  daylint.textContent = `$ ${dayli.toLocaleString()}`;
  rtotal.textContent = `$ ${total.toLocaleString()}`;
};

cashInput.addEventListener('input', updateValues);
intsInput.addEventListener('input', updateValues);
montInput.addEventListener('input', updateValues);
