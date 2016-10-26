var autocomplete =(function ($) {

    var searchField = $('.form-dropdown .form-dropdown-input'),
        results = $('.form-dropdown-results'),
        tags = $('.form-dropdown-tags');

    searchField.keyup(catchEvent);
    searchField.keypress(function (event) {
        // User press enter
        if (event.which === 13 && $('.form-dropdown-option').length > 0) {
            event.preventDefault();
            selectedFirst();
        }
    });

    $('html').click(function (event) {
        if(!$(event.target).hasClass('form-dropdown-input')) {
            closeDropdown();
        }
    });

    function selectedFirst() {
        addTag.call($('.form-dropdown-option').first());
    }


    function catchEvent(event) {

        switch(event.which) {
            case 40:
                selectOption('down');
                break;
            case 38:
                selectOption('up');
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

                $(element).next().append('<li><a href="" class="form-dropdown-option" data-option-id="' + option + '">' + content + '</li></a></li>');
            }
            $('.form-dropdown-option').on('click', addTag);
        }
    }

    function addTag() {

        event.preventDefault();

        var caterogyId = $(this).data('option-id'),
            checkboxOption = $(this).parent().parent().prev().data('field');
        $(this).parent().parent().next().append('<li>'+$(this).text()+' <button href="" data-option-id="'+caterogyId+'" class="form-dropdown-tags--close">x</button> </li>');
        $('.form-dropdown-tags--close').on('click', deleteTag);
        addCheckbox(checkboxOption, caterogyId);
        resultCount.update_count();
        closeDropdown();
    }

    function deleteTag() {
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

        $('.filters-checkbox').append(input);
    }

    function deleteCheckbox(checkboxId) {
        $('input[data-checkbox-id="'+checkboxId+'"]').remove();
    }

    function selectOption(action){
        console.log(action);
        // var selector = "#artist-" + index;
        // $('.highlighted').removeClass('highlighted');
        // $(selector).addClass('highlighted');
    }


})(jQuery);