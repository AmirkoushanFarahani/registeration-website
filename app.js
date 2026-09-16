const form = document.querySelector('#registration-form');
const error = document.querySelector('#form-error');
const success = document.querySelector('#success');

function toEnglishDigits(value) {
  return value.replace(/[۰-۹]/g, d => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d)).replace(/[٠-٩]/g, d => '٠١٢٣٤٥٦٧٨٩'.indexOf(d));
}

function validNationalId(value) {
  const code = toEnglishDigits(value).replace(/\D/g, '');
  if (!/^\d{10}$/.test(code) || /^(\d)\1{9}$/.test(code)) return false;
  const total = [...code.slice(0, 9)].reduce((sum, digit, index) => sum + Number(digit) * (10 - index), 0);
  const check = total % 11 < 2 ? total % 11 : 11 - (total % 11);
  return check === Number(code[9]);
}

form.addEventListener('submit', event => {
  event.preventDefault();
  error.hidden = true;
  const data = new FormData(form);
  const phone = toEnglishDigits(data.get('parentPhone')).replace(/\D/g, '');
  if (!form.checkValidity()) {
    error.textContent = 'لطفاً همه فیلدهای الزامی را تکمیل کنید.';
    error.hidden = false;
    form.querySelector(':invalid').focus();
    return;
  }
  if (!validNationalId(data.get('nationalId'))) {
    error.textContent = 'کد ملی واردشده معتبر نیست.';
    error.hidden = false;
    form.elements.nationalId.focus();
    return;
  }
  if (!/^09\d{9}$/.test(phone)) {
    error.textContent = 'شماره همراه ولی باید با ۰۹ شروع شود و ۱۱ رقم باشد.';
    error.hidden = false;
    form.elements.parentPhone.focus();
    return;
  }
  document.querySelector('#tracking-code').textContent = `IR-${Date.now().toString().slice(-8)}`;
  success.hidden = false;
  success.scrollIntoView({ behavior: 'smooth', block: 'center' });
  form.reset();
});
