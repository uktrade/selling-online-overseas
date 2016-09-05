var menu = (function ($) {
    var toggleButton = $('.header-nav-toggle'),
        menu = $('.header-nav');

    toggleButton.click({ button: toggleButton, menu: menu }, toggle);

    function toggle (event){
        event.preventDefault();
        $(event.data.button).toggleClass('header-nav-toggle--open');
        $(event.data.menu).toggleClass( "open");
    }

    return {
        toggle: toggle
    };

})(jQuery);
