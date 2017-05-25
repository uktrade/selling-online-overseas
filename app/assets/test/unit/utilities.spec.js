describe('Utilties', function () {

    it('Should navigate to previous page', function () {

        sinon.stub(window.history, 'back');

        utilities.navigateBack();

        expect(window.history.back.calledOnce).to.be.true;
    })
});