var utilities = (function ($) {

    $('*[data-scrollTo]').on('click', scrollTo);


    function navigateBack() {
        window.history.back();
    }

    function scrollTo(event) {
        event.preventDefault();
        var element = $('#'+$(event.target).data('scrollto'));
        $("body,html").animate({ scrollTop: element.position().top }, 500);
    }

    return {
        navigateBack: navigateBack,
        scrollTo: scrollTo
    };

})(jQuery);
