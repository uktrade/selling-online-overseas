var sortList = (function () {

    var shortlist = $('.markets-shortlist'),
        removeAllButton = $('.shortlist-remove');

    shortlist.click(shortList);
    removeAllButton.click(removeAll);

    function init() {
        $.ajax({
            url: '/markets/api/shortlist/',
            type: 'GET',
            success:function(result) {
                result.market_slugs.forEach(function(slug){
                    var element = $('[data-slug=' + slug + ']'),
                        icon = $(element[0].lastChild);
                    element.addClass('markets-shortlist--shortlisted');
                    icon.addClass('icon-shortlisted');
                });
            }
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
            }, 800);
    }

    function shortList(event) {
        event.preventDefault();

        var element = $(event.target),
            icon = $(element[0].lastChild),
            slug = element.data('slug');


        if(element.hasClass('markets-shortlist--shortlisted')) {

            $.ajax({
                url: '/markets/api/shortlist/?slug='+slug,
                type: 'DELETE',
                success:function() {
                    element.removeClass('markets-shortlist--shortlisted');
                    icon.removeClass('icon-shortlisted');
                    notify('shortlist-notify','marketplace removed from your shortlist', element );
                }
            });
        } else {
            $.ajax({
                url: '/markets/api/shortlist/?slug='+slug,
                type: 'POST',
                success:function() {
                    element.addClass('markets-shortlist--shortlisted');
                    icon.addClass('icon-shortlisted');
                    notify('shortlist-notify','marketplace added to your shortlist', element );
                }
            });
        }

    }
    function removeAll(event) {
        event.preventDefault();
        // $.ajax({
        //     url: '/markets/api/shortlist/',
        //     type: 'REMOVE',
        //     success:function() {
        //         location.reload();
        //     }
        // });

    }

    return {
        init: init
    };

}(jQuery));

sortList.init();