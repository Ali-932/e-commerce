
// // Service worker registration
// if ('serviceWorker' in navigator) {
//     navigator.serviceWorker.register( "static/js/custom_js/service-worker.js")
//         .then(function (registration) {
//             console.log('Service worker registered with scope:', registration.scope);
//         })
//         .catch(function (error) {
//             console.log('Service worker registration failed:', error);
//         });
// }

// Install prompt logic
let deferredPrompt;
const installModal = document.getElementById('installModal');
const installButton = document.getElementById('installButton');
const closeModal = document.getElementById('closeModal');

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    if (isMobileDevice()) {
        // Show the install prompt modal
        installModal.style.display = 'block';
    }
});

installButton.addEventListener('click', (e) => {
    // Hide the modal
    installModal.style.display = 'none';
    // Show the install prompt
    deferredPrompt.prompt();
    // Wait for the user to respond to the prompt
    deferredPrompt.userChoice.then((choiceResult) => {
        deferredPrompt = null;
    });
});

// Close the modal when the user clicks on <span> (x)
closeModal.onclick = function () {
    installModal.style.display = 'none';
};

// Close the modal if the user clicks anywhere outside of the modal
window.onclick = function (event) {
    if (event.target == installModal) {
        installModal.style.display = 'none';
    }
};

function isMobileDevice() {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}