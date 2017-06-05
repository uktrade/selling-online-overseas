var tooltip = (function ($) {

    var tooltipButton = $('.tooltip-button');

    tooltipButton.click(openDialog);

    function openDialog (event) {
        var selected = $(this).data('tooltip'),
            selector = 'dialog[data-tooltip="' + selected + '"]',
            target = $(event.target);


        if(target.hasClass('tooltip-button--expanded')) {
            $(event.target).removeClass('tooltip-button--expanded');
            removeDialog(selector);
        } else {
            target.addClass('tooltip-button--expanded');
            $(selector).append(createDialog(target.data('tooltip-text')));
            setAttributes(selector, selected);
        }
    }

    function createDialog(text) {
        return  '<div role="document">'+
                    '<p class="tooltip-title simple-tooltip-tooltip__title">'+text+'</p>'+
                '</div>';
    }

    function removeDialog(selector) {
        $(selector).children().remove();
    }

    function setAttributes(element, data) {
        $(element ).attr({
            role: 'dialog',
            'aria-labelledby': 'tooltip-title',
            'data-tooltip': data
        });

        $(element).addClass('tooltip-text');
    }


})(jQuery);
