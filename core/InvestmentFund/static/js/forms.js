
const inputs = document.querySelectorAll('input[name="ammount_from"]');

let AVIABLE_VALUE = Number(available).valueOf();
let BENEFIT_VALUE = Number(ref_available).valueOf();
let CASHTLL_VALUE = Number(cash_total).valueOf();

let MINAMMOUNT = Number(min_ammount).valueOf();
let FEE = Number(fee).valueOf();

let FAVIABLE_VALUE = AVIABLE_VALUE.toLocaleString();
let FBENEFIT_VALUE = BENEFIT_VALUE.toLocaleString();
let FCASHTLL_VALUE = CASHTLL_VALUE.toLocaleString();

inputs.forEach(input => {
    input.addEventListener('change', function() {
    const value = this.value;
    if (value === 'f1') {
        document.getElementById('title').innerHTML = '$Disponible Intereses:';
        document.getElementById('aviable_value').innerHTML = "$"+FAVIABLE_VALUE;
        document.getElementById('ammount').value = AVIABLE_VALUE;
        document.getElementById('ammount').min = MINAMMOUNT + FEE;
        document.getElementById('ammount').max = AVIABLE_VALUE;
    } else if (value === 'f2') {
        document.getElementById('title').innerHTML = '$Disponible Comiciones:';
        document.getElementById('aviable_value').innerHTML = "$"+FBENEFIT_VALUE;
        document.getElementById('ammount').value = BENEFIT_VALUE;
        document.getElementById('ammount').min = MINAMMOUNT + FEE;
        document.getElementById('ammount').max = BENEFIT_VALUE;
    } else if (value === 'f3') {
        document.getElementById('title').innerHTML = '$Disponible Total:';
        document.getElementById('aviable_value').innerHTML = "$"+FCASHTLL_VALUE;
        document.getElementById('ammount').value = CASHTLL_VALUE;
        if (CASHTLL_VALUE < MINAMMOUNT + FEE) {
            document.getElementById('ammount').min = MINAMMOUNT + FEE;
        } else {
            document.getElementById('ammount').min = CASHTLL_VALUE;
            document.getElementById('ammount').max = CASHTLL_VALUE;
        }
    }
    });
});
