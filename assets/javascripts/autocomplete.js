var autocomplete =(function ($) {

    var searchField = $('.filters-category-search'),
        results = $('.filters-results'),
        tags = $('.tags');

    searchField.keyup(getResults);

    function getResults() {

        var categories = $.ajax({
            url: '/products/api/',
            type: 'GET',
            dataType: 'json',
            data: { q: $(this).val() }
        });

        $.when(categories)
            .done(function(categories) {
                createDropDown(categories);
            })
            .fail(function() {
            })
            .always(function() {
            });
    }

    function createDropDown(data) {
        closeDropdown();
        for(var i = 0; i < data.categories.length; i++) {
            results.append('<li><a href="" class="filter-caterory" data-category-id="'+data.categories[i][0]+'">' + data.categories[i][0] + ' - <strong>'+data.categories[i][1]+'</strong></li></a></li>');
        }
        $('.filter-caterory').on('click', addTag);
    }

    function addTag() {

        event.preventDefault();

        var caterogyId = $(this).data('category-id');
        tags.append('<li>'+$(this).text()+' <a href="" data-category-id="'+caterogyId+'" class="tags-close">x</a> </li>');
        $('.tags-close').on('click', deleteTag);
        addCheckbox('product_categories', caterogyId);
        resultCount.update_count();
        closeDropdown();
    }

    function deleteTag() {
        event.preventDefault();
        $(this).parent().remove();
        deleteCheckbox($(this).data('category-id'));
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


})(jQuery);