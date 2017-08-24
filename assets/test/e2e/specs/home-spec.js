var settings = require('../settings/settings'),
    home = require('../settings/home'),
    list = require('../settings/list');

describe('Selling Online Overseas homepage', function() {

    beforeEach(function () {
        browser.ignoreSynchronization = true;
    });

    it('Should be on the homepage', function() {
        browser.get(settings.navigate.home);
        expect(home.pageHeader.getText()).toEqual('Find online marketplaces');
    });

    describe('Marketplace filter', function () {

        it('Should have the number all of marketplace', function () {
            expect(home.results.getText()).not.toBe('');
        });

        it('Should display a list of countries', function () {
            home.countryInputField.sendKeys('a');
            expect((home.countryDropdown).count()).toBeGreaterThan(0)
        });

        it('Should select a country and create a country tag', function () {
            var numberOfMarketplace = home.results.getText();
            home.countryDropdown.get(0).click();
            expect(home.tagsList.count()).toEqual(1);
            browser.refresh();
            expect(home.results.getText()).not.toEqual(numberOfMarketplace);
        });

        it('Should display a list of products', function () {
            home.productInputField.sendKeys('health');
            expect((home.productDropdown).count()).toBeGreaterThan(0)
        });

        it('Should select a product and create a product tag', function () {
            var numberOfMarketplace = home.results.getText();
            home.productDropdown.get(0).click();
            expect(home.tagsList.count()).toEqual(2);
            browser.refresh();
            expect(home.results.getText()).not.toEqual(numberOfMarketplace);
        });

        it('Should delete a product tag', function () {
            var numberOfMarketplace = home.results.getText();
            home.tagsList.get(1).click();
            expect(home.tagsList.count()).toEqual(1);
            browser.refresh();
            expect(home.results.getText()).not.toEqual(numberOfMarketplace);
        });

        it('Should delete a country tag', function () {
            var numberOfMarketplace = home.results.getText();
            home.tagsList.get(0).click();
            expect(home.tagsList.count()).toEqual(0);
            browser.refresh();
            expect(home.results.getText()).not.toEqual(numberOfMarketplace);
        });

        xit('Should scroll to find marketplace form', function () {
            browser.actions().mouseMove(home.scrollToFormButton).perform();
            home.scrollToFormButton.click();
            expect(home.scrollToFormButton.getLocation()).toEqual('10');

            browser.pause();
        });

        it('Should navigate to list page', function () {
            var numberOfMarketplace = home.results.getText();
            home.findMarketplaceButton.click();
            expect(list.marketsCount.getText()).toContain(numberOfMarketplace);
        });

    });

});



