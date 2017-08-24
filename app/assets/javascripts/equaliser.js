var equaliser = (function ($) {
    var section = $("div[data-equaliser]"),
        height = 0;

    if(section.length > 0) {
        equaliseHeight();
        $(window).resize(equaliseHeight);
    }

    function equaliseHeight() {
        $.each(section, function (index, value) {
            var divs = $(value).find("div[data-section]");
            $.each(divs, function (index, value) {
                if ($(value).outerHeight() > height) {
                    height = $(value).outerHeight();
                }
            });

            $.each(divs, function (index, value) {
                $(value).height(height);
            });
        });
    }


})(jQuery);
