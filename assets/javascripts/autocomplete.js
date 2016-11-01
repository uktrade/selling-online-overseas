var autocomplete =(function ($) {

    var searchField = $('.form-dropdown .form-dropdown-input'),
        results = $('.form-dropdown-results'),
        tags = $('.form-dropdown-tags');

    searchField.keyup(catchEvent);
    searchField.keypress(function (event) {
        // User press enter
        if (event.which === 13 && $('.form-dropdown-option').length > 0) {
            event.preventDefault();
            selectedEnter();
        }
    });

    $('html').click(function (event) {
        if(!$(event.target).hasClass('form-dropdown-input')) {
            closeDropdown();
        }
    });

    function selectedEnter() {
        var option = ($('.form-dropdown-results li.active a').length === 0) ? $('.form-dropdown-option').first() : $('.form-dropdown-results li.active a');
        addTag.call(option);
    }


    function catchEvent(event) {

        var nextElement = $(event.target).next();

        switch(event.which) {
            case 40:
                selectOption('down', nextElement);
                break;
            case 38:
                selectOption('up', nextElement);
                break;
            case 13:
                event.preventDefault();
                break;
            case 27:
                closeDropdown();
                break;
            default:
                getResults(this);
        }

    }

    function getResults(element) {

        var categories = $.ajax({
            url: $(element).data('url'),
            type: 'GET',
            dataType: 'json',
            data: {q: $(element).val()}
        });

        var test = element;

        $.when(categories)
            .done(function (categories) {
                createDropDown(categories, test);
            })
            .fail(function () {
            })
            .always(function () {
            });
    }

    function createDropDown(request, element) {
        closeDropdown();

        var data = request.countries ? request.countries : request.categories;

        if(data) {
            for (var i = 0; i < data.length; i++) {
                var content = (typeof(data[i]) === 'string') ? data[i] : data[i][0] + ' - <strong>'+data[i][1]+'</strong>',
                    option = (typeof(data[i]) === 'string') ? data[i] : data[i][0];

                $(element).next().append('<li class="form-dropdown-list"><a href="" class="form-dropdown-option" data-option-id="' + option + '">' + content + '</li></a></li>');
            }
            $('.form-dropdown-option').on('click', addTag);
        }
    }

    function addTag(event) {
        event.preventDefault();
        var caterogyId = $(this).data('option-id'),
            checkboxOption = $(this).parent().parent().prev().data('field');
        $(this).parent().parent().next().append('<li>'+$(this).text()+' <button href="" data-option-id="'+caterogyId+'" class="form-dropdown-tags--close">x</button> </li>');
        $('.form-dropdown-tags--close').on('click', deleteTag);
        addCheckbox(checkboxOption, caterogyId);
        resultCount.update_count();
        closeDropdown();
    }

    function deleteTag(event) {
        event.preventDefault();
        $(this).parent().remove();
        deleteCheckbox($(this).data('option-id'));
        resultCount.update_count();
    }

    function closeDropdown() {
        results.empty();
    }
    
    function addCheckbox(field, value) {
        var input = $('<input>', {
            type:"checkbox",
            name: field,
            value: value,
            checked: true,
            'data-checkbox-id': value
        });

        $('.form-dropdown-checkbox').append(input);
    }

    function deleteCheckbox(checkboxId) {
        $('input[data-checkbox-id="'+checkboxId+'"]').remove();
    }

    function selectOption(action, element){

        var list = (element.children().length - 1),
            active = $('.form-dropdown-results li.active').index();

        if(!$('.form-dropdown-results li').hasClass('active')) {
            $($('.form-dropdown-results li')[0]).addClass('active');
        } else {
            $($('.form-dropdown-results li')[active]).removeClass('active');
            if(action === 'up') {
                $($('.form-dropdown-results li')[active-1]).addClass('active');
            } else {
                var option = (active === list) ? 0 : active+1;
                $($('.form-dropdown-results li')[option]).addClass('active');
            }

        }
    }


})(jQuery);