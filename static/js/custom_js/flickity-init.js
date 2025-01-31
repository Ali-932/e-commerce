// flickity-init.js
// Alpine.js carousel initialization
function carousel() {
    return {
        active: 0,
        init() {
            var flkty = new Flickity(this.$refs.carousel, {
                wrapAround: true
            });
            flkty.on('change', i => this.active = i);
        }
    }
}

function carouselFilter() {
    return {
        active: 0,
        changeActive(i) {
            this.active = i;
            this.$nextTick(() => {
                let flkty = Flickity.data(this.$el.querySelectorAll('.carousel')[i]);
                flkty.resize();
            });
        }
    }
}

document.body.addEventListener('htmx:beforeSwap', function () {
    return {
        active: 0,
        changeActive(i) {
            this.active = i;
            this.$nextTick(() => {
                let flkty = Flickity.data(this.$el.querySelectorAll('.carousel')[i]);
                flkty.resize();
            });
        }
    }
});

// Flickity reinitialization after HTMX loads or swaps
document.body.addEventListener('htmx:afterOnLoad', function () {
    setTimeout(function () {
        var carouselElements = document.querySelectorAll('.carousel');
        carouselElements.forEach(function (element) {
            var flkty = Flickity.data(element);
            if (flkty) {
                flkty.reloadCells();
                flkty.resize();
                flkty.updateDraggable();
            } else {
                flkty = new Flickity(element, { wrapAround: true });
                // Example: If you want to update some Alpine property:
                flkty.on('change', function (index) {
                    if (typeof xData !== 'undefined' && xData.carouselFilter) {
                        xData.carouselFilter.active = index;
                    }
                });
            }
        });
    }, 100);
});