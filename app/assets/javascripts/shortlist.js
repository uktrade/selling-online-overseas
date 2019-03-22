var sortList = (function () {

    var shortlist = $('.markets-shortlist'),
        removeAllButton = $('.shortlist-remove'),
        apiUrl = '/selling-online-overseas/markets/api/shortlist/';

    shortlist.click(shortList);
    removeAllButton.click(removeAll);

    function init() {
        var success_handler,
            homepage_info = $('#homepage-shortlist-info'),
            markets_list = $('.markets-list, .markets-grid');

        if (homepage_info.length) {
            success_handler = function(result) {
                if (result.market_slugs.length) {
                    homepage_info.show();
                }
            };
        }

        if (markets_list.length) {
            success_handler = function(result) {
                markShortlistedMarkets(result.market_slugs);
            };
        }

        updateShortlistedCount(success_handler);
    }

    function markShortlistedMarkets(market_slugs) {
        market_slugs.forEach(function(slug) {
            var element = $('[data-slug=' + slug + ']'),
                icon = $(element[0].lastChild);
            updateState(element, icon, 'Shortlisted');
        });
    }

    function notify(classname, text, element) {
        var notify = $('<span>', {
            html: text,
            'class': classname
        });


        element.append(notify);

        setTimeout(function() {
           notify.remove();
            }, 2000);
    }

    function shortList(event) {
        event.preventDefault();

        var element = $(event.currentTarget),
            icon = $(element[0].lastChild),
            slug = element.data('slug');


        if(element.hasClass('markets-shortlist--shortlisted')) {

            $.ajax({
                url: apiUrl+'?slug='+slug,
                type: 'DELETE',
                success:function() {
                    updateState(element, icon, 'Shortlist');
                    if(sessionStorage.getItem('notify') !== '2') {
                        notify('shortlist-notify','Marketplace removed from your shortlist', element );
                        sessionStorage.setItem('notify', 2);
                    }
                    updateShortlistedCount();
                }
            });
        } else {
            $.ajax({
                url: apiUrl+'?slug='+slug,
                type: 'POST',
                success:function() {
                    updateState(element, icon, 'Shortlisted');
                    if(!sessionStorage.getItem('notify')) {
                        notify('shortlist-notify','Marketplace added to your shortlist', element );
                        sessionStorage.setItem('notify', 1);
                    }
                    updateShortlistedCount();
                }
            });
        }

    }

    function updateState(element, icon, action) {
        if (action === 'Shortlisted') {
            element.addClass('markets-shortlist--shortlisted');
            icon.addClass('icon-shortlisted');
        } else {
            element.removeClass('markets-shortlist--shortlisted');
            icon.removeClass('icon-shortlisted');
        }

        element.contents()[0].textContent = action;
    }

    function updateShortlistedCount(additional_handler) {
        $.ajax({
            url: apiUrl,
            type: 'GET',
            success:function(result) {
                $('.shortlist-count').html(result.market_slugs.length);
                if (typeof additional_handler !== 'undefined') {
                    additional_handler(result);
                }
            }
        });
    }

    function removeAll(event) {
        event.preventDefault();
        $.ajax({
            url: apiUrl,
            type: 'DELETE',
            success:function() {
                location.reload();
            }
        });

    }

    $(document).ready(init);

    return {
        init: init
    };

}(jQuery));
