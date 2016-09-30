var filter = (function ($) {
    var tabItem = $('.filters-tab--item'),
        closeButton = $('.button-close'),
        filterOptions = $('.filters-options'),
        form = $('.filters-form'),
        filterFields = $('.filters-form input');

    tabItem.click({tabs: tabItem, filters: filterOptions}, toggle);
    closeButton.click({tabs: tabItem, filters: filterOptions}, closeForm);
    filterFields.change({form: form}, updateMarketList);


    function toggle(event) {
        event.preventDefault();
        var clickTab = $(this),
            selector = '.filters-options' + '[data-field="' + $(event.target).data("group") + '"]',
            selectedGroup = $(selector)[0];

        $(event.data.filters).hide();

        if (clickTab.hasClass('active')) {
            $(event.data.tabs).removeClass('active');
            $(selectedGroup).hide();
            form.hide();
        } else {
            $(event.data.tabs).removeClass('active');
            clickTab.addClass('active');
            $(selectedGroup).show();
            form.show();
        }
    }

    function updateMarketList(event) {

        var data = event.data.form.serialize(),
            getMarkets = $.ajax({
                url: '/markets/api/',
                type: 'GET',
                dataType: 'html',
                data: data
            }),
            getMarketCount = $.ajax({
                url: '/markets/count.json',
                type: 'GET',
                dataType: 'json',
                data: data
            });

        $('body').prepend("<div class='loader'></div>");

        $.when(getMarkets, getMarketCount)
            .done(function(getMarkets, getMarketCount) {
               $('ul.markets').html(getMarkets[0]);
               $('.heading-results').html(setTitle(getMarketCount[0].count));
            })
            .fail(function() {
                /* TODO display error msg, if something wrong happens */
            })
            .always(function() {
                $('.loader').remove();
            });
    }

    function setTitle(markets) {
        return markets+' marketplace'+(markets > 1 ? 's':'')+' found';
    }


    function closeForm(event) {
        event.preventDefault();
        $(event.data.tabs).removeClass('active');
        $(event.data.filters).hide();
        form.hide();
    }

    return {
        toggle: toggle,
        closeForm: closeForm,
        updateMarketList: updateMarketList,
        setTitle: setTitle
    };

})(jQuery);
