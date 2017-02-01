var validationMessages = (function () {

    var messages = {
        'company': {
            'name': 'Please type in your company name.',
            'search': 'Please search for your company name.',
            'number': 'Please provide your company number.',
            'no_number': 'If you don\'t have a company number please tick this box.',
            'postcode' : 'Please tell us the postcode of your business.',
            'website': 'Please give us your website address or a link where your products are shown.'
        },
        'business': {
            'turnover': 'Please select an option which best describes your turnover.',
            'sku': 'Please give us the number of your stock keeping units.',
            'trademark': 'Please select an option to indicate if your products are trademarked or not.'
        },
        'experience': {
            'export': 'Please select an option which best describes your experience in selling online abroad.',
            'introduction': 'Please write a few paragraphs about your business and products.'
        },
        'contact' :{
            'name': 'Please give us a contact name.',
            'email': 'Please give us a valid email address.',
            'phone': 'Please give us a valid phone number'
        }
    };


    return {
        messages: messages
    };

})();