var triageForm = function ($) {

    var activeTab = 0,
        navigateButton = $('.form-tab-section a'),
        tabCompletedlinks = $('a.form-tab-link--completed');

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
        $($('.form-tab-section')[selectedFrom]).addClass('show');
        $('.form-tab-section').addClass('hide');
    }

    function checkTabsStatus(selectedTab) {
        $($('.form-tab li a')[selectedTab]).addClass('form-tab-link--active');

        if(selectedTab>=0) {
            setCompletedTab(selectedTab);
        }
    }

    function setCompletedTab(selectedTab) {
        selectedTab--;
        $($('.form-tab li a')[selectedTab]).removeClass('form-tab-link--active').addClass('form-tab-link--completed');
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

        deActiveSection(activeTab);

        switch(action) {
            case 'next':
                activeTab++;
                break;
            case 'back':
                $($('.form-tab li a')[activeTab]).removeClass('form-tab-link--active form-tab-link--completed');
                activeTab--;
                break;
            default:
                $('.form-tab li a').removeClass('form-tab-link--active form-tab-link--completed');
                activeTab = $(".form-tab-link").index( $(event.currentTarget));
        }

        activeSection(activeTab);
    }


    return {
        init: init
    };
}(jQuery);

triageForm.init();