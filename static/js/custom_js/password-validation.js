// password-validation.js
function setupPasswordValidation() {
    const password1 = document.querySelector('#id_password1');
    const password2 = document.querySelector('#id_password2');

    if (password1) {
        password1.addEventListener('input', function () {
            validatePassword1();
            if (password2 && password2.value.length > 0) {
                validatePassword2();
            }
        });
    }

    if (password2) {
        password2.addEventListener('input', validatePassword2);
    }

    function validatePassword1() {
        const numericPattern = /^[0-9]+$/;
        let message = '';

        if (password1.value.length < 8) {
            message = 'لابد ان يكون الرمز السري عل اقل 8 احرف.';
        }
        if (numericPattern.test(password1.value)) {
            message = 'لابد ان يحتوي الرمز السري على احرف';
        }

        if (message) {
            displayError(password1, message);
        } else {
            removeError(password1);
        }
    }

    function validatePassword2() {
        let message = '';
        if (password2.value !== password1.value && password2.value.length !== 0) {
            message = 'الرمز السري لا يتطابق.';
        }

        if (message) {
            displayError(password2, message);
        } else {
            removeError(password2);
        }
    }

    function getErrorElement(input) {
        const parent = input.parentElement;
        let errorElem = parent.querySelector('.invalid-feedback');
        if (!errorElem) {
            errorElem = document.createElement('div');
            errorElem.className = 'invalid-feedback';
            parent.appendChild(errorElem);
        }
        return errorElem;
    }

    function displayError(input, message) {
        const errorElem = getErrorElement(input);
        errorElem.innerText = message;
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
    }

    function removeError(input) {
        const parent = input.parentElement;
        const errorElem = parent.querySelector('.invalid-feedback');
        if (errorElem) {
            errorElem.remove();
        }
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    }
}

// Attach the validation setup to relevant events
['htmx:afterSwap', 'DOMContentLoaded'].forEach(function (eventName) {
    document.addEventListener(eventName, setupPasswordValidation);
});