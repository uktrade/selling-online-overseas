var settings = require('../settings/settings'),
    list = require('../settings/list');


describe('list page', function() {

    beforeEach(function () {
        browser.ignoreSynchronization = true;
    });

    it('Should be on the list page', function() {
        browser.get(settings.navigate.list);
        expect(list.marketsCount.getText()).toContain(list.resultsList.count());
    });

    it('should navigate to first marketplace', function () {
        list.resultsList.first().element(by.tagName('.markets-info')).click();
        expect(element(by.tagName('h1')).getText()).not.toBe('');
    })

});
