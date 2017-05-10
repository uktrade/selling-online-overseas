var utilities = (function ($) {

    function navigateBack() {
        window.history.back();
    }

    return {
        navigateBack: navigateBack
    };

})(jQuery);
