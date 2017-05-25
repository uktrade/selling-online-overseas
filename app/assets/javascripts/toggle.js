var toggle = (function ($) {

    $('a[data-toggle="button"]').click(function (event) {
        event.preventDefault();
        $(this).parent().parent().find('[data-toggle="container"]').toggle();
        $(this).find('i').toggleClass('icon-close');
    });

})(jQuery);