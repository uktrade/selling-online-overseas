var formIntro = (function ($) {
    var button = $(".form-intro-button"),
        section = $('.form-intro-content');

    button.click(function () {
        section.toggle();
        $(this).toggleClass( "form-intro-button--open" );
    });

})(jQuery);
