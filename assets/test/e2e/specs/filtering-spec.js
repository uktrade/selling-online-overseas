var settings = require('../settings/settings'),
    home = require('../settings/home'),
    filtering = require('../settings/filtering');

describe('Filtering Page', function() {

    beforeEach(function () {
        browser.ignoreSynchronization = true;
        browser.get(settings.navigate.filtering);

    });

    describe('Should be on filtering page', function () {

        it('Should have a sub header', function() {
            browser.get(settings.navigate.home);
            home.startButton.click();
            expect(element(by.css('.sub-heading')).getText()).toEqual('Please use the filters to narrow down your results');
        });

        it('Should see the number all of markets', function () {
            expect(filtering.results.getText()).not.toBe('');
        });

        it('Should have a list of countries', function () {
            expect((filtering.countryList).count()).toBeGreaterThan(1)
        })
    });

    describe('Should filter by country', function () {
        it('Should update online marketplaces listed', function() {
            var initialResult = filtering.results.getText();
            filtering.countryList.get(4).click();
            browser.sleep(1000);
            expect(filtering.results.getText()).not.toEqual(initialResult);
        });
    });

    describe('Should filter by product category', function () {
        it('Should update online marketplaces listed', function() {
            var initialResult = filtering.results.getText();
            filtering.productList.get(5).click();
            browser.sleep(1000);
            expect(filtering.results.getText()).not.toEqual(initialResult);
        });
    });

    describe('Should filter by product type', function () {
        it('Should update online marketplaces listed', function() {
            var initialResult = filtering.results.getText();
            filtering.productTypeModelOption.click();
            browser.sleep(1000);
            expect(filtering.results.getText()).not.toEqual(initialResult);
        });
    });

    describe('Should filter by seller model ', function () {
        it('Should update number of online marketplaces listed', function () {
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