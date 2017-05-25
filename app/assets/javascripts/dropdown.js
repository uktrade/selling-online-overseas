var dropdown = (function ($) {

    function manualSelect(event) {
        var nextElement = $(event.currentTarget);

        switch(event.which) {
            case 40:
                event.preventDefault();
                selectOption('down', nextElement);
                break;
            case 38:
                event.preventDefault();
                selectOption('up', nextElement);
                break;
            default:
                break;
        }
    }

    function selectOption(action, element) {

        var list = (element.children().length - 1),
            active = $('.form-dropdown-results li.active').index();

        if(!$('.form-dropdown-results li').hasClass('active')) {
            activateAndFocus(0);
        } else {
            $($('.form-dropdown-results li')[active]).removeClass('active');
            $($('.form-dropdown-results li a')[active]).blur();
            if(action === 'up') {
                activateAndFocus((active === 0) ? 0 : active-1);
            } else {
                activateAndFocus((active === list) ? 0 : active+1);
            }
        }
    }

    function activateAndFocus(index) {
        $($('.form-dropdown-results li')[index]).addClass('active');
        $($('.form-dropdown-results li a')[index]).focus();
    }

    function closeDropdown() {
        $('.form-dropdown-results').empty().hide();
        $('html').removeClass('overflow--hidden');
    }

    return {
        manualSelect: manualSelect,
        selectOption: selectOption,
        closeDropdown: closeDropdown
    };

})(jQuery);
