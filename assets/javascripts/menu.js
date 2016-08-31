var menu = (function ($) {
    var toogleButtom = $('.header-nav-toggle'),
        menu = $('.header-nav');

    toogleButtom.click(function(event) {
        event.preventDefault();
        $(this).toggleClass('header-nav-toggle--open');
        menu.toggleClass( "open");
    });

})(jQuery);
