module.exports = {
    results: element(by.css('#results-count h4')),
    resultsButton: element(by.css('.button-result')),
    productTypeModelOption: element(by.css('#id_product_type_0')),
    listHeaderResults: element(by.css('.heading-results')),
    countryList: element(by.id('countries_served')).all(by.tagName('option')),
    productList: element(by.id('product_categories')).all(by.tagName('option'))
};