module.exports = {
    pageHeader: element(by.css('h1.h1')),
    results: element(by.css('#results-count .results-count')),
    countryInputField: element(by.css('#search-country')),
    countryDropdown: element(by.css('#search-country +ul')).all(by.tagName('li a')),
    productInputField: element(by.css('#search-country')),
    productDropdown: element(by.css('#search-country +ul')).all(by.tagName('li a')),
    tagsList: element(by.css('.form-dropdown-tags')).all(by.tagName('li button')),
    findMarketplaceButton: element(by.css('#results-count button')),
    scrollToFormButton: element(by.css('.steps-sub-section button'))
};