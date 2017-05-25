var feedback = (function ($) {

    var button_container = $('.thumber-radio-buttons'),
        buttons = $('.thumber-form button'),
        radio_input_container = $('.thumber-radio-inputs'),
        radio_inputs = $('.thumber-form input[type=radio]');

    radio_input_container.hide();
    button_container.show();
    buttons.on('click', handleClick);

    function handleClick(event) {
        var value = $(event.currentTarget).data('value');
        event.preventDefault();
        radio_inputs.filter('[value=' + value + ']').click();
        buttons.attr("disabled", true);


    }

    var displaySuccess = function () {
        $('.audit').html($('.audit-thank').html());
    };

    var displayError = function () {
        $('.audit').html($('.audit-error').html());
    };

    return {
        displaySuccess: displaySuccess,
        displayError: displayError
    };

}(jQuery));

$(document).ready(function() {
    if (typeof thumber !== 'undefined') {
        thumber.setSuccessHandler(feedback.displaySuccess);
        thumber.setErrorHandler(feedback.displayError);
    }
});