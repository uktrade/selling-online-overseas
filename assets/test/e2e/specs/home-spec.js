var settings = require('../settings/settings'),
    home = require('../settings/home');

describe('Marketplace homepage', function() {

    beforeEach(function () {
        browser.ignoreSynchronization = true;
    });

    it('Should be on the homepage', function() {
        browser.get(settings.navigate.home);
        expect(home.startButton.getText()).toEqual('Start now');
    });

});
