var settings = require('../settings/settings'),
    list = require('../settings/list'),
    detail = require('../settings/detail');

describe('details page', function() {


    beforeEach(function () {
        browser.ignoreSynchronization = true;
    });

    it('Should be on the details page', function() {
        browser.get(settings.navigate.list);
        list.resultsList.first().element(by.tagName('.markets-info')).click();
        expect(browser.getCurrentUrl()).toContain('/markets/details/');

    });

    describe('Should navigate to triage form', function () {

        it('Should click on the top apply button', function () {
            var marketplaceName = settings.pageHeader.getText();
            detail.applyButton.click();
            expect(settings.pageHeader.getText()).toEqual(marketplaceName);
        });

        it('Should click on the bottom apply button', function () {
            browser.get(settings.navigate.list);
            list.resultsList.first().element(by.tagName('.markets-info')).click();
            var marketplaceName = settings.pageHeader.getText();
            detail.bottomApplyButton.click();
            expect(settings.pageHeader.getText()).toEqual(marketplaceName);
        })
    });

    describe('should navigate to the marketplace page', function () {

        it('Should click on the go to marketplace button', function () {

            browser.get(settings.navigate.list);
            list.resultsList.first().element(by.tagName('.markets-info')).click();

            detail.goToMarketplaceButton.each(function (element) {
                element.getAttribute('href').then(function(attr) {
                    var url = attr.replace(/(^\w+:|^)\/\//, '');
                    detail.goToMarketplaceButton.click();
                    expect(browser.getCurrentUrl()).toContain(url);
                });
            });
        })
    })
});
