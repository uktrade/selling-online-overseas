var formIntro = (function ($) {
    var button = $(".form-intro-button"),
        section = $('.form-intro-content');

    button.click(function (event) {
        event.preventDefault();
        section.toggle();
        $(this).find("i").toggleClass( "icon-close" );
    });

})(jQuery);
