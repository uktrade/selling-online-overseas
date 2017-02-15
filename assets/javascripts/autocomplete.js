var autoComplete =(function ($) {

    var searchField = $('.form-dropdown .form-dropdown-input'),
        results = $('.form-dropdown-results'),
        cachedTags = {
            'operating_countries': [],
            'product_categories': []
        };

    function init() {

        if($('form').data('form-type') === "autocomplete") {

            searchField.keyup(inputEvent);
            results.keyup(dropdown.manualSelect);
            searchField.keypress(function (event) {
                // User press enter
                if (event.which === 13 && $('.form-dropdown-option').length > 0) {
                    event.preventDefault();
                    selectedEnter();
                }
            });

            $('html').click(function (event) {
                var input = $(event.target);
                if (!input.hasClass('form-dropdown-input') || input.val() === "") {
                    dropdown.closeDropdown();
                    var inputs = $('.form-dropdown-input');
                    inputs.each(function (i, item) {
                        var input = $(item);
                        if (input.val() !== '') {
                            clearInput(input);
                        }
                    });
                }
            });

            updateTagsFromStorage();
        }
    }

    function selectedEnter() {
        var option = ($('.form-dropdown-results li.active a').length === 0) ? $('.form-dropdown-option').first() : $('.form-dropdown-results li.active a');
        addTag.call(option);
    }

    function inputEvent(event) {

        var nextElement = $(event.target).next();

        switch(event.which) {
            case 40:
                event.preventDefault();
                dropdown.selectOption('down', nextElement);
                break;
            case 13:
                event.preventDefault();
                break;
            case 27:
                var input = $(event.target);
                dropdown.closeDropdown();
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
        dropdown.closeDropdown();

        var list = $(element).next();

        for (var i = 0; i < request.length; i++) {
            var content = (typeof(request[i]) === 'string') ? request[i] : '<b>'+request[i][0]+'</b>'+ ' - '+request[i][1],
                option = (typeof(request[i]) === 'string') ? request[i] : request[i][0],
                isSelected = _.contains(cachedTags[$(element).data('field')], option) ? 'form-dropdown-option--selected' : '';

            console.log(isSelected);

            list.append('<li class="form-dropdown-list" role="option"><a href="" class="form-dropdown-option '+isSelected+'" data-option-id="' + option + '">' + content + '</li></a></li>');
        }

        list.show();
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

        if(checkDuplicateTag(optionId, checkboxOption)) {
            return;
        }

        createTag($('.form-dropdown-tags'), checkboxOption, optionId, buttonId);
        resultCount.update_count();

        clearInput(input);
        dropdown.closeDropdown();
        addTagToStorage(buttonId, optionId, checkboxOption);
    }

    function checkDuplicateTag(optionId, checkboxOption) {

        if(!(_.contains(cachedTags[checkboxOption], optionId ))) {
            cachedTags[checkboxOption].push(optionId);
        } else {
            animateSelected($('button[data-option-id="'+optionId+'"]').first().parent());
            return true;
        }

    }

    function animateSelected(selected) {
        selected.addClass('shake-vertical');

        setTimeout(function () {
            selected.removeClass("shake-vertical");
        }, 1000);
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

        var button = $('<button>', {
            'data-button-id': buttonId,
            'data-option-id': optionId,
            'data-item': checkboxOption,
            class: "form-dropdown-tags--close",
            html: "x"
        }),
        li = $('<li>', {
            class: (checkboxOption==='operating_countries' ? 'background--light-aqua' : 'background--stone'),
            html: optionId + button[0].outerHTML
        });


        container.append(li);
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
        var optionId = $(this).data('option-id');

        event.preventDefault();
        $(this).parent().remove();
        deleteCheckbox(optionId);
        resultCount.update_count();
        deleteTagFromStorage($(event.target).data('button-id'));
        deleteCacheTag($(this).data('item'),optionId);
    }

    function deleteCacheTag(key, value) {
        cachedTags[key] = _.filter(cachedTags[key], function(val){ return val !== value; });
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

    function updateTagsFromStorage() {
        if(sessionStorage.getItem('tags')) {
            _.each(JSON.parse(sessionStorage.getItem('tags')), function (obj) {
                var element = (obj.section === 'product_categories') ? 'search-product' : 'search-country';
                if (obj.section && obj.option) {
                    createTag($('.form-dropdown-tags'), obj.section, obj.option, obj.buttonId);
                    checkDuplicateTag(obj.option, obj.section);
                } else {
                    deleteTagFromStorage(obj.buttonId);
                }
            });
        }
    }

    return {
        init: init,
        selectedEnter: selectedEnter,
        inputEvent: inputEvent,
        getResults: getResults,
        createDropDown: createDropDown,
        addTag: addTag,
        createTag: createTag,
        clearInput: clearInput,
        addTagToStorage: addTagToStorage,
        deleteTagFromStorage: deleteTagFromStorage,
        deleteTag: deleteTag,
        addCheckbox: addCheckbox,
        deleteCheckbox: deleteCheckbox,
        updateTagsFromStorage: updateTagsFromStorage
    };

})(jQuery);

$(document).ready(function() {
    autoComplete.init();
});

