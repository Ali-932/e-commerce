// scroll-to-top.js
function scrollToTop() {
    const scrollPosition = window.scrollY || document.documentElement.scrollTop;
    if (scrollPosition > 100) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}