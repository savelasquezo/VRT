
const inputs = document.querySelectorAll('input[name="ammount_from"]');

let AVIABLE_VALUE = Number(available).valueOf();
let BENEFIT_VALUE = Number(ref_available).valueOf();

let MINAMMOUNT = Number(min_ammount).valueOf();
let TAXES = Number(fee).valueOf();

let FAVIABLE_VALUE = AVIABLE_VALUE.toLocaleString();
let FBENEFIT_VALUE = BENEFIT_VALUE.toLocaleString();

document.getElementById('ammount').min = MINAMMOUNT + TAXES;

inputs.forEach(input => {
    input.addEventListener('change', function() {
    const value = this.value;
    if (value === 'f1') {
        document.getElementById('title').innerHTML = '$Disponible Intereses:';
        document.getElementById('aviable_value').innerHTML = "$"+FAVIABLE_VALUE;
        document.getElementById('ammount').value = AVIABLE_VALUE;
        document.getElementById('ammount').max = AVIABLE_VALUE;

    } else if (value === 'f2') {
        document.getElementById('title').innerHTML = '$Disponible Comiciones:';
        document.getElementById('aviable_value').innerHTML = "$"+FBENEFIT_VALUE;
        document.getElementById('ammount').value = BENEFIT_VALUE;
        document.getElementById('ammount').max = BENEFIT_VALUE;

    }
    });
});
