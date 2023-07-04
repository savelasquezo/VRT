$(document).ready(function(){
    var carousel = $('.owl-carousel');
    carousel.owlCarousel({
        loop: true,
        rewind: false,
        margin: 0,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: true
            },
            600: {
                items: 3,
                nav: false
            },
            1000: {
                items: 5,
                nav: true,
            }
        },
        autoplay: true,
        autoplayTimeout: 2000,
        autoplayHoverPause: true,
        animateOut: 'slideOutUp',
        smartSpeed: 2000,
    });
});
