const input = document.getElementById('amount');
const currencyRadios = document.querySelectorAll('input[name="currency"]');
let currentCurrency = '';
function setMaxValue(currency) {
  if (currency === 'COP') {
    input.max = 300000000;
  } else if (currency === 'USD') {
    input.max = 100000;
  }
}
currencyRadios.forEach(function (radio) {
  radio.addEventListener('change', function () {
    const newCurrency = this.value;
    if (newCurrency !== currentCurrency) {
      setMaxValue(newCurrency);
      currentCurrency = newCurrency;
      const valorIngresado = parseFloat(input.value);
      const max = parseFloat(input.max);
      if (valorIngresado > max) {
        input.value = max;
      }
    }
  });
});
setMaxValue(currencyRadios[0].value);
input.addEventListener('input', function () {
  const valorIngresado = parseFloat(input.value);
  const max = parseFloat(input.max);
  if (valorIngresado > max) {
    input.value = max;
  }
});