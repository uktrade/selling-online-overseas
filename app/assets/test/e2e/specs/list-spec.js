var settings = require('../settings/settings'),
    list = require('../settings/list');


describe('list page', function() {

    beforeEach(function () {
        browser.ignoreSynchronization = true;
    });

    it('Should be on the list page', function() {
        browser.get(settings.navigate.list);
        expect(settings.pageHeader.getText()).toContain(list.resultsList.count());
    });

    it('should navigate to first markplace', function () {
        list.resultsList.first().element(by.tagName('.button-blue')).click();
        expect(element(by.tagName('h1')).getText()).not.toBe('');
    })

});
