for (eve of ['htmx:afterSwap', 'DOMContentLoaded']) {

    document.addEventListener(eve, function () {
        registrationForm = document.getElementById('registrationForm')
        if (registrationForm) {
            registrationForm.addEventListener('submit', function (e) {
                // Track the CompleteRegistration event
                fbq('track', 'CompleteRegistration', {});
                fbq('track', 'Lead', {})
            });
        }
    });
}