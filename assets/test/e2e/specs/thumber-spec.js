var settings = require('../settings/settings'),
    thumber  = require('../settings/thumber');

describe('Thumber', function() {

    beforeEach(function () {
        browser.ignoreSynchronization = true;
    });

    it('Should click on yes', function() {
        browser.get(settings.navigate.home);
        thumber.yesButton.click();
        expect(thumber.thankYouHeader.getText()).toEqual(thumber.thankYouMessage);
    });

    it('Should click on yes', function() {
        browser.get(settings.navigate.home);
        thumber.noButton.click();
        expect(thumber.noButton.getAttribute('disabled')).toEqual('true');
        expect(thumber.yesButton.getAttribute('disabled')).toEqual('true');
    });


    it('Should send feedback message', function() {
        thumber.thankComments.sendKeys('Awesome page');
        thumber.sendButton.click();
        browser.sleep(10000);
        expect(thumber.thankYouHeader.getText()).toEqual(thumber.thankYouMessage);
    });

});
