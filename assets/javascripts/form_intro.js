var formIntro = (function ($) {
    var button = $(".form-intro-button"),
        section = $('.form-intro-content');

    button.click(function () {
        section.toggle();
        $(this).children().toggleClass( "icon-close" );
    });

})(jQuery);
