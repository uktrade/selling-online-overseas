var autocomplete =(function ($) {

    var searchField = $('.form-dropdown .form-dropdown-input'),
        results = $('.form-dropdown-results'),
        tags = $('.form-dropdown-tags');


    function init() {

        searchField.keyup(catchEvent);
        searchField.keypress(function (event) {
            // User press enter
            if (event.which === 13 && $('.form-dropdown-option').length > 0) {
                event.preventDefault();
                selectedEnter();
            }
        });

        $('html').click(function (event) {
            var input = $(event.target);
            if(!input.hasClass('form-dropdown-input')) {
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
                var content = (typeof(data[i]) === 'string') ? data[i] : data[i][0] + ' - '+data[i][1]+'',
                    option = (typeof(data[i]) === 'string') ? data[i] : data[i][0];

                $(element).next().append('<li class="form-dropdown-list"><a href="" class="form-dropdown-option" data-option-id="' + option + '">' + content + '</li></a></li>');
            }
            $('.form-dropdown-option').on('click', addTag);
        }
    }

    function addTag(event) {

        var link  = event ? $(event.target) : $(this),
            input = link.parent().parent().prev(),
            buttonId = Math.round(Math.random()*(+new Date())),
            categoryId = $(this).data('option-id'),
            checkboxOption = $(this).parent().parent().prev().data('field'),
            text = $(this).text();

        if (event) {
            event.preventDefault();
        }

        createTag($(this).parent().parent().next(), checkboxOption, text, categoryId, buttonId);
        resultCount.update_count();

        clearInput(input);
        closeDropdown();
        addTagToStorage(buttonId, categoryId, text, checkboxOption);
    }

    function createTag(container, checkboxOption, text, categoryId, buttonId) {
        container.append('<li>'+text+'<button href="" data-option-id="'+categoryId+'" class="form-dropdown-tags--close" data-button-id="'+buttonId+'">x</button></li>');
        $('.form-dropdown-tags--close').on('click', deleteTag);
        addCheckbox(checkboxOption, categoryId);
    }

    function clearInput(input) {
        dataLayer.push({"event": "Search", "search_term": input.val()});
        input.val("");
    }

    function addTagToStorage(buttonId, categoryId, data, section) {

        function Tag(buttonId, categoryId, data, section) {
            this.buttonId = buttonId;
            this.category = categoryId;
            this.content = data;
            this.section = section;
        }

        var tags = sessionStorage.getItem('tags') ? JSON.parse(sessionStorage.getItem('tags')) : [];
        tags.push(new Tag(buttonId, categoryId, data, section));

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

    function updateTagsFromStorage() {
        if(sessionStorage.getItem('tags')) {
            _.each(JSON.parse(sessionStorage.getItem('tags')), function (obj) {
                var element = (obj.section === 'product_categories') ? 'search-product' : 'search-country';
                createTag($('#'+element).next().next(), obj.section, obj.content, obj.category, obj.buttonId);
            });
        }
    }

    return {
        init: init
    };
})(jQuery);

autocomplete.init();