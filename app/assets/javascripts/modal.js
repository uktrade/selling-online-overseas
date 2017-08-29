var modal = (function ($) {

    $('*[data-modal-button]').click(openModal);
    $('*[data-action="close-modal"]').click(closeModal);


    function openModal(event) {
        event.preventDefault();
        $('[data-modal-id='+$(event.target).data('modal-button')+']').show();
    }

    function closeModal(event) {
        event.preventDefault();
        $(event.currentTarget).closest('.modal').hide();
    }

    return {
        openModal: openModal,
        closeModal: closeModal
    };

})(jQuery);