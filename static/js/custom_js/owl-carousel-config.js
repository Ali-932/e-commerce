// owl-carousel-config.js
// Store Owl Carousel configuration objects
var owlCarouselOptions = {
    nav: false,
    dots: true,
    loop: true,
    responsive: {
        0:   { items: 1.5 },
        480: { items: 2 },
        768: { items: 4 },
        992: { items: 4 },
        1200: {
            items: 4,
            nav: true,
            dots: true
        }
    }
};

var owlCarouselOptions2 = {
    nav: false,
    dots: true,
    loop: false,
    responsive: {
        0:   { items: 1.5 },
        480: { items: 2 },
        768: { items: 3 },
        992: { items: 3.5 },
        1200: {
            items: 3.5,
            nav: true,
            dots: true
        }
    }
};

var owlCarouselOptionsSide = {
    nav: false,
    dots: true,
    margin: 10,
    autoplay: true,
    loop: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    responsive: {
        0:   { items: 1 },
        480: { items: 1 },
        768: { items: 1 },
        992: { items: 1 },
        1200:{ items: 1 }
    }
};

// Initialize Owl Carousel on page load
$(document).ready(function () {
    initOwlCarousel();
});

// Reinitialize Owl Carousel on htmx afterSettle event
$(document).on('htmx:afterSettle', function () {
    setTimeout(function () {
        initOwlCarousel();
    }, 0);
});

// Function to initialize or reinitialize Owl Carousel
function initOwlCarousel() {
    $('.owl-carousel').each(function () {
        var $carouselContainer = $(this);
        // Check if the carousel is already initialized
        if (typeof $carouselContainer.data('owl.carousel') === 'undefined') {
            // Initialize the carousel with the stored configuration
            if (this.id === 'myCarousel') {
                $carouselContainer.owlCarousel(owlCarouselOptions);
            } else if (this.id === 'CarouselLatest') {
                $carouselContainer.owlCarousel(owlCarouselOptions2);
            } else if (this.id === 'CarouselSideLatest') {
                $carouselContainer.owlCarousel(owlCarouselOptionsSide);
            }

            // Update Owl Carousel's internal settings
            $carouselContainer.trigger('refresh.owl.carousel');
        }
    });
}