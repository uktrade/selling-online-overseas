var triageForm = function ($) {

    var activeTab = 0,
        navigateButton = $('.form-tab-section a');

    function init() {
        activeSection(activeTab);
        navigateButton.click(navigate);
        $('.form-tab').on('click', 'a.form-tab-link--completed', navigate);
    }

    function activeSection(index) {
        checkTabsStatus(index);
        checkFormStatus(index);
        setProgressBar(index);
    }

    function checkFormStatus(selectedFrom) {
        $('.form-tab-section').addClass('hide').removeClass('show');
        $($('.form-tab-section')[selectedFrom]).addClass('show');
    }

    function checkTabsStatus(selectedTab) {

        $('.form-tab li a').removeClass('form-tab-link--active form-tab-link--completed');


        if(selectedTab>=0) {
            setCompletedTab(selectedTab);
        }
        $($('.form-tab li a')[selectedTab]).addClass('form-tab-link--active');
    }

    function setCompletedTab(selectedTab) {
        selectedTab--;
        if(selectedTab >=0) {
            $($('.form-tab li a')[selectedTab]).removeClass('form-tab-link--active').addClass('form-tab-link--completed');
            setCompletedTab(selectedTab);
        }
    }

    function deActiveSection(tab) {
        $($('.form-tab-section')[tab]).addClass('hide');
        $($('.form-tab-section')[tab]).removeClass('show');
    }

    function setProgressBar(tab) {
        var item = (tab===0) ? 1 : tab+1,
            progress = item/($('.form-tab li a').length)*100;

        $('.form-tab-progressbar-indicator').width(progress+'%');
    }

    function navigate(event) {

        event.preventDefault();
        var action = $(event.currentTarget).data('action');

        switch(action) {
            case 'next':
                deActiveSection(activeTab);
                activeTab++;
                break;
            case 'back':
                deActiveSection(activeTab);
                activeTab--;
                break;
            default:
                activeTab = $(".form-tab-link").index( $(event.currentTarget));
        }
        activeSection(activeTab);
        window.location.hash = $(this).attr("href");
    }


    return {
        init: init
    };
}(jQuery);

triageForm.init();