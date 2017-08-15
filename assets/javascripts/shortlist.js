var sortList = (function () {

    var shortlist = $('.markets-shortlist');

    shortlist.click(shortList);

    function init() {

    }


    function shortList(event) {
        event.preventDefault();

        var element = $(event.target),
            icon = $($(event.target)[0].lastChild),
            slug = $(event.target).data('slug');


        if(element.hasClass('markets-shortlist--shortlisted')) {
            element.removeClass('markets-shortlist--shortlisted');
            icon.removeClass('icon-shortlisted');
            // $.ajax({
            //     url: '/markets/api/shortlist/remove/'+slug,
            //     type: 'GET',
            //     success:function(result) {
            //         console.log('remove to shortlist');
            //     }
            // });
        } else {
            element.addClass('markets-shortlist--shortlisted');
            icon.addClass('icon-shortlisted');
            // $.ajax({
            //     url: '/markets/api/shortlist/add/'+slug,
            //     type: 'GET',
            //     success:function(result) {
            //         console.log('added to shortlist');
            //     }
            // });
        }

    }

    return {
        init: init
    };

}(jQuery));

sortList.init();