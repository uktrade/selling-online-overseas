var settings = require('../settings/settings'),
    home = require('../settings/home'),
    filtering = require('../settings/filtering');

describe('Filtering Page', function() {

    beforeEach(function () {
        browser.ignoreSynchronization = true;
    });

    describe('Should be on filtering page', function () {
        it('Should be on the filtering page', function() {
            browser.get(settings.navigate.home);
            home.startButton.click();
            expect(element(by.css('.sub-heading')).getText()).toEqual('Please use the filters to narrow down your results');
            expect(filtering.results.getText()).not.toBe('');
        });
    });

    describe('Should filter by product catalogue', function () {
        it('Should update number of ecommerce site listed', function () {

            var initialResult = filtering.results.getText();
            filtering.sellerModelOption.click();
            browser.sleep(1000);
            expect(filtering.results.getText()).not.toEqual(initialResult);
        });

        it('Should navigate to list page', function () {
            var filteredResult = filtering.results.getText();
            filtering.resultsButton.click();
            expect(filtering.listHeaderResults.getText()).toContain(filteredResult);
        });
    });

});