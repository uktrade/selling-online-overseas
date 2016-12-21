var search =(function ($) {

    var searchField = $('.form-dropdown .form-dropdown-input'),
        results = $('.form-dropdown-results'),
        tags = $('.form-dropdown-tags');


    function init() {

        searchField.keyup(inputEvent);
        results.keyup(manualSelect);
        searchField.keypress(function (event) {
            // User press enter
            if (event.which === 13 && $('.form-dropdown-option').length > 0) {
                event.preventDefault();
                selectedEnter();
            }
        });

        $('html').click(function (event) {
            var input = $(event.target);
            if(!input.hasClass('form-dropdown-input') || input.val()=== "") {
                closeDropdown();
                var inputs = $('.form-dropdown-input');
                inputs.each(function(i, item) {
                    var input = $(item);
                    if (input.val() !== '') {
                        clearInput(input);
                    }
                });
            }
        });

        updateTagsFromStorage();
    }



    function selectedEnter() {
        var option = ($('.form-dropdown-results li.active a').length === 0) ? $('.form-dropdown-option').first() : $('.form-dropdown-results li.active a');
        addTag.call(option);
    }


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

    function inputEvent(event) {

        var nextElement = $(event.target).next();

        switch(event.which) {
            case 40:
                event.preventDefault();
                selectOption('down', nextElement);
                break;
            case 13:
                event.preventDefault();
                break;
            case 27:
                var input = $(event.target);
                closeDropdown();
                clearInput(input);
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

        $.when(categories)
            .done(function (categories) {
                var data = categories.countries ? categories.countries : categories.categories;

                if(data.length > 0) {
                    createDropDown(data, element);
                }
            })
            .fail(function () {
            })
            .always(function () {
            });
    }

    function createDropDown(request, element) {
        closeDropdown();

        for (var i = 0; i < request.length; i++) {
            var content = (typeof(request[i]) === 'string') ? request[i] : '<b>'+request[i][0]+'</b>'+ ' - '+request[i][1],
                option = (typeof(request[i]) === 'string') ? request[i] : request[i][0];

            $(element).next().append('<li class="form-dropdown-list" role="option"><a href="" class="form-dropdown-option" data-option-id="' + option + '">' + content + '</li></a></li>');
        }

        $('.form-dropdown-option').click(addTag);
        $('.form-dropdown-list').hover(onHover);
        $('html').addClass('overflow--hidden');
    }

    function addTag(event) {

        var link  = event ? $(event.target) : $(this),
            input = link.parent().parent().prev(),
            buttonId = Math.round(Math.random()*(+new Date())),
            optionId = $(this).data('option-id'),
            checkboxOption = $(this).parent().parent().prev().data('field');

        if (event) {
            event.preventDefault();
        }

        createTag($(this).parent().parent().next(), checkboxOption, optionId, buttonId);
        resultCount.update_count();

        clearInput(input);
        closeDropdown();
        addTagToStorage(buttonId, optionId, checkboxOption);
    }

    function onHover() {
        $('.form-dropdown-list').removeClass('active');

        if (!$(this).hasClass('active')) {
            $(this).addClass('active');
            $(this).children().focus();
        } else {
            $(this).removeClass('active');
        }
    }

    function createTag(container, checkboxOption, optionId, buttonId) {
        container.append('<li>'+optionId+'<button href="" data-option-id="'+optionId+'" class="form-dropdown-tags--close" data-button-id="'+buttonId+'">x</button></li>');
        $('.form-dropdown-tags--close').on('click', deleteTag);
        addCheckbox(checkboxOption, optionId);
    }

    function clearInput(input) {
        dataLayer.push({"event": input.attr('id'), "search_term": input.val()});
        input.val("");
    }

    function addTagToStorage(buttonId, optionId, section) {

        function Tag(buttonId, optionId, section) {
            this.buttonId = buttonId;
            this.option = optionId;
            this.section = section;
        }

        var tags = sessionStorage.getItem('tags') ? JSON.parse(sessionStorage.getItem('tags')) : [];
        tags.push(new Tag(buttonId, optionId, section));

        sessionStorage.setItem('tags', JSON.stringify(tags));
    }

    function deleteTagFromStorage(id) {
        var tags = _.reject(JSON.parse(sessionStorage.getItem('tags')),function(obj){ return obj.buttonId === id; });
        sessionStorage.setItem('tags', JSON.stringify(tags));
    }

    function deleteTag(event) {
        event.preventDefault();
        $(this).parent().remove();
        deleteCheckbox($(this).data('option-id'));
        resultCount.update_count();
        deleteTagFromStorage($(event.target).data('button-id'));
    }

    function closeDropdown() {
        results.empty();
        $('html').removeClass('overflow--hidden');
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
        $('input[data-checkbox-id="'+checkboxId+'"]').first().remove();
    }

    function selectOption(action, element){

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

    function updateTagsFromStorage() {
        if(sessionStorage.getItem('tags')) {
            _.each(JSON.parse(sessionStorage.getItem('tags')), function (obj) {
                var element = (obj.section === 'product_categories') ? 'search-product' : 'search-country';
                if (obj.section && obj.option) {
                    createTag($('#'+element).next().next(), obj.section, obj.option, obj.buttonId);
                } else {
                    deleteTagFromStorage(obj.buttonId);
                }
            });
        }
    }

    return {
        init: init
    };
})(jQuery);

search.init();