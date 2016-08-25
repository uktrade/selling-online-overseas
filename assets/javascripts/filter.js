var filter = (function ($) {
    var tabItem = $('.filters-tab--item'),
        closeButton = $('.button-close'),
        filterOptions = $('.filters-options');

    tabItem.click({tabs: tabItem, filters: filterOptions}, toggle);
    closeButton.click({tabs: tabItem, filters: filterOptions}, closeForm);

    function toggle(event) {
        event.preventDefault();
        var clickTab = $(this),
            selector = '.filters-options' + '[data-field="' + $(event.target).data("group") + '"]',
            selectedGroup = $(selector)[0];

        $(event.data.filters).hide();

        if (clickTab.hasClass('active')) {
            $(event.data.tabs).removeClass('active');
            $(selectedGroup).hide();
        } else {
            $(event.data.tabs).removeClass('active');
            clickTab.addClass('active');
            $(selectedGroup).show();
        }
    }
    
    function closeForm(event) {
        event.preventDefault();
        $(event.data.tabs).removeClass('active');
        $(event.data.filters).hide();
    }

    return {
        toggle: toggle,
        closeForm: closeForm
    };

})(jQuery);
