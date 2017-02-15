var audit = (function ($) {

    var form = $('.audit-form'),
        buttons = $('.audit-form button'),
        textarea = $('.audit-text-section'),
        id;

    buttons.on('click', handleForm);

    function handleForm(event) {

        event.preventDefault();

        var data = {
            'feedback_token': 'ajax',
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        };

        switch($(event.currentTarget).data('audit')) {
            case 'no':
                data.satisfied = 'False';

                $.when(feedbackRequest(data))
                    .done(function (response) {
                        id = response.id;
                        $(event.currentTarget).attr("disabled", true);
                        textarea.removeClass('hide');
                    })
                    .fail(function () {
                        displayMessage('error');
                    });
                break;
            case 'yes':
                data.satisfied = 'True';

                $.when(feedbackRequest(data))
                    .done(function () {
                        displayMessage('successful');
                    })
                    .fail(function () {
                        displayMessage('error');
                    });
                break;
            default:
                data.id = id;
                data.comment = $('.audit-form .form-textarea').val();

                $.when(feedbackRequest(data))
                    .done(function () {
                        displayMessage('successful');
                    })
                    .fail(function () {
                        displayMessage('error');
                    });
        }
    }



    function feedbackRequest(data) {

        var feedback = $.ajax({
            url: form.attr('action'),
            type: 'POST',
            dataType: 'json',
            data: data
        });

        return feedback;
    }

    function displayMessage(status) {

        var  statusClass = '.audit-error';

        if(status === "successful") {
            statusClass = '.audit-thank';
        }

        $('.audit').html($(statusClass).html());
        formSteps.scrollTo($('.audit'));
    }

}(jQuery));
