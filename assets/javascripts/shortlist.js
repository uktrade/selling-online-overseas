var sortList = (function () {

    var shortlist = $('.markets-shortlist');

    shortlist.click(shortList);

    function init() {

    }


    function shortList(event) {
        event.preventDefault();

        var slug = $(event.target).data('slug');


        if($(event.target).hasClass('markets-shortlist--shortlisted')) {
            $.ajax({
                url: '/markets/api/shortlist/remove/'+slug,
                type: 'GET',
                success:function(result) {
                    console.log('remove to shortlist');
                }
            });
        } else {
            $.ajax({
                url: '/markets/api/shortlist/add/'+slug,
                type: 'GET',
                success:function(result) {
                    console.log('added to shortlist');
                }
            });
        }

    }

    return {
        init: init
    };

}(jQuery));

sortList.init();