var sortList = (function () {

    var shortlist = $('.markets-shortlist');

    shortlist.click(shortList);

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
                }
            });
        } else {
            $.ajax({
                url: '/markets/api/shortlist/?slug='+slug,
                type: 'POST',
                success:function() {
                    element.addClass('markets-shortlist--shortlisted');
                    icon.addClass('icon-shortlisted');
                }
            });
        }

    }

    return {
        init: init
    };

}(jQuery));

sortList.init();