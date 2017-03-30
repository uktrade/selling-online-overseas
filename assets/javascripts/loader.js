var loader = (function ($) {


    function add() {
        var loader = '<span class="loader"></span>';

        if($( 'span.loader' ).length === 0 ) {
            $('body').append(loader);
         }
    }

    function remove() {
        $('.loader').remove();
    }

    return {
        add: add,
        remove: remove
    };

})(jQuery);