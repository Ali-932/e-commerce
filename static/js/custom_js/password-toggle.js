// password-toggle.js
for (eve of ['htmx:afterSwap', 'DOMContentLoaded']) {
    document.addEventListener(eve, function () {
        for (i of [1, 2, 3]) {
            const togglePassword = document.querySelector(`#password${i}Button`);
            const password = document.querySelector(`#id_password${i}`);
            if (togglePassword && password) {
                togglePassword.addEventListener('click', function () {
                    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
                    password.setAttribute('type', type);

                    if (this.firstChild.classList.contains('fa-eye-slash')) {
                        this.firstChild.classList.remove('fa-eye-slash');
                        this.firstChild.classList.add('fa-eye');
                    } else {
                        this.firstChild.classList.remove('fa-eye');
                        this.firstChild.classList.add('fa-eye-slash');
                    }
                });
            }
        }
    });
}