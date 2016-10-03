var utilities = (function ($) {

    var backButton = $('.link--back');

    backButton.click(navigateBack);

    function navigateBack() {
        window.history.back();
    }

    return {
        navigateBack: navigateBack
    };

})(jQuery);