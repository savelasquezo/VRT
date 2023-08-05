$(document).ready(function(){
    var carousel = $('.owl-carousel');
    carousel.owlCarousel({
        loop: true,
        center: true,
        rewind: false,
        responsiveClass: true,
        responsive:{
            0:{
                items:1,
                margin: 3,
            },
            600:{
                items:3,
                margin: 5,
            },
            1000:{
                items:5,
                margin: 7,
            }
        },
        autoplay: true,
        animateOut: 'fadeOut',
        autoplayTimeout: 2000,
        autoplayHoverPause: true,
        smartSpeed: 2000,
    });
});
