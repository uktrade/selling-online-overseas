var sorting = (function () {

    $('#sort input, #sort-select').change(sortList);

    function init() {

        $("#sort input[type=radio], #sort-select option").each(function() {
            if(getParameterByName('sort') === $(this)[0].value ) {
                var property = (($(this)[0].tagName).toLowerCase() === 'option') ? "selected" : "checked";
                $(this).prop(property, true);
            }
        });
    }

    function getParameterByName(name) {
        name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");

        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    }

    function sortList(event) {

        var sortBy;

        event.preventDefault();
        loader.add();

        if(($(this)[0].tagName).toLowerCase() === 'input') {
            sortBy = $("#sort input:checked")[0].value;
        } else {
            sortBy = $(this).find("option:selected").attr('value');
        }

        setTimeout(function(){
            window.location.href = location.pathname+'?'+$('#results-form').serialize()+'&sort='+sortBy;
        }, 100);
    }

    return {
        init: init
    };

}(jQuery));

sorting.init();