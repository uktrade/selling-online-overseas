var validation = function ($) {

    var elements = [];

    function validateFields() {
        var valid = true,
            fields  = $('.form-tab-section.show *[data-validate]');

        if($('.form-group').hasClass('form-group-error')) {
            clearErrorMessage();
        }

        for(var i=0; i<fields.length;i++) {
            var validation = $(fields[i]).data('validate');

            switch (validation) {
                case 'company':
                    if(isEmpty(fields[i])) {
                        displayErrorMessage(fields[i], validationMessages.messages.company.name);
                        valid = false;
                    }
                    break;
                case 'company-number':
                    if(isEmpty(fields[i]) && notCheck($('.form-tab-section.show *[data-validate="soletrader"]'), 'soletrader') ) {
                        displayErrorMessage(fields[i], validationMessages.messages.company.number);
                       valid = false;
                    }
                    break;
                case 'postcode':
                    if(isEmpty(fields[i])) {
                        displayErrorMessage(fields[i], validationMessages.messages.company.postcode);
                       valid = false;
                    }
                    break;
                case 'url':
                    if(isEmpty(fields[i])) {
                        displayErrorMessage(fields[i], validationMessages.messages.company.website);
                       valid = false;
                    }
                    break;
                case 'sku':
                    if(isEmpty(fields[i])) {
                        displayErrorMessage(fields[i], validationMessages.messages.business.sku);
                        valid = false;
                    }
                    break;
                case 'description':
                    if(isEmpty(fields[i])) {
                        displayErrorMessage(fields[i], validationMessages.messages.experience.introduction);
                        valid = false;
                    }
                    break;
                case 'name':
                    if(isEmpty(fields[i])) {
                        displayErrorMessage(fields[i], validationMessages.messages.contact.name);
                        valid = false;
                    }
                    break;
                case 'email':
                    if(isEmpty(fields[i]) || (!isValidEmail($(fields[i]).val()))) {
                        displayErrorMessage(fields[i], validationMessages.messages.contact.email);
                        valid = false;
                    }
                    break;
                case 'contact-number':
                    if(isEmpty(fields[i])) {
                        displayErrorMessage(fields[i], validationMessages.messages.contact.phone);
                        valid = false;
                    }
                    break;
                case 'turnover':
                    if(notCheck(fields[i], validation)) {
                        displayErrorMessage(fields[i], validationMessages.messages.business.turnover);
                        valid = false;
                    }
                    break;
                case 'trademark':
                    if(notCheck(fields[i], validation)) {
                        displayErrorMessage(fields[i], validationMessages.messages.business.trademark);
                        valid = false;
                    }
                    break;
                case 'export':
                    if(notCheck(fields[i], validation)) {
                        displayErrorMessage(fields[i], validationMessages.messages.experience.export);
                        valid = false;
                    }
                    break;
                default:
            }
        }
        return valid;
    }

    function isValidEmail(email) {
        var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        return regex.test(email);
    }

    function notCheck(field, validation) {
        var checked = true,
            fields = $('.form-tab-section.show *[data-validate='+validation+']');

        elements.push(field);

        for(var i=0; i<fields.length;i++) {
            if($(fields[i]).is(':checked')) {
                checked = false ;
            }
        }

        if(fields.length === elements.length) {
            elements = [];
            return checked;
        }
    }

    function isEmpty( field) {
        return ($(field).val() === "");
    }

    function displayErrorMessage(field, message) {
        $(field).closest('.form-group').addClass('form-group-error').prepend('<span class="form-group-error--message">'+message+'</span>');
    }

    function clearErrorMessage() {
        $('.form-group-error--message').remove();
        $('.form-group').removeClass('form-group-error');
    }

    return {
        validateFields: validateFields
    };

}(jQuery);