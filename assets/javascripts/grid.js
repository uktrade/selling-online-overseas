var grid = (function () {

    var gridSection = $('ul.markets');

    $('*[data-sort]').click(updateGrid);

    function updateGrid(event) {
        event.preventDefault();

        $('.markets-views button').removeClass('markets-views--active');

        var action = $(event.currentTarget).data('sort');

        console.log($(event.currentTarget));

        if(action === 'grid') {

            gridSection.addClass('markets-grid markets-grid--three shortlist-list');
        } else {
            gridSection.removeClass('markets-grid markets-grid--three shortlist-list');
        }

        $(event.currentTarget).addClass('markets-views--active');

    }

}(jQuery));
