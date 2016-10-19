var tooltip = (function ($) {

    var tooltipButton = $('.tooltip-button');

    tooltipButton.click(openDialog);

    function openDialog (event) {
        var selected = $(this).data('tooltip'),
        selector = '.tooltip-text' + '[data-tooltip="' + selected + '"]';

        if($(event.target).hasClass('tooltip-button--expanded')) {
            $(event.target).removeClass('tooltip-button--expanded');
            $(selector).removeClass('tooltip-text--active');
        } else {
            $(event.target).addClass('tooltip-button--expanded');
            $(selector).addClass('tooltip-text--active');
        }




    }

})(jQuery);
