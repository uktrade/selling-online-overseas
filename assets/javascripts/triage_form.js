var triageForm = function ($) {

    var activeTab = 0,
        navigateButton = $('.form-tab-section a');



    function init() {
        activeSection(activeTab);
        navigateButton.click(navigate);

    }

    function activeSection(tab) {
        $($('.form-tab li a')[tab]).addClass('form-tab-link--active');
        $($('.form-tab-section')[tab]).addClass('show');
        $('.form-tab-section').addClass('hide');
        setProgressBar(tab);
    }

    function setProgressBar(tab) {
        var item = (tab===0) ? 1 : tab,
            progress = item/($('.form-tab li a').length)*100;

        $('.form-tab-progressbar-indicator').width(progress+'%');
        activeTab = item;
    }

    function navigate(event) {
        var action = $(event.currentTarget).data('action');

        if(action === "next") {
            console.log(activeTab++);
        } else {
            console.log(activeTab--);
        }


    }



    return {
        init: init
    };
}(jQuery);

triageForm.init();