describe('Mobile Navigation', function() {

    var toggleButton,
        navigation,
        e,
        html ='<div class="menu">' +
                '<a href="" class="navigation-main-button" title="">menu</a>' +
                '<nav>' +
                    '<ul class="navigation-toggle" style="display: none">' +
                        '<li class="navigation-toggle-item"><a title="" href="" class="active">home</a></li>' +
                    '</ul>' +
                '</nav>' +
              '</div>';

    function init() {

        toggleButton = $('.navigation-main-button'),
        navigation = $('.navigation-toggle'),
        e = {
            preventDefault: sinon.spy(),
            data: {
                button: toggleButton,
                menu: navigation
            }
        };
    }


    before(function() {
        $('body').append(html);
        init();
    });

    describe('Click on Menu button', function () {

        it('Should display navigation', function () {

            menu.toggle(e);

            expect(toggleButton.hasClass('navigation-main-button--open')).to.be.true;
            expect(navigation.hasClass('navigation-toggle--open')).to.be.true;

        });

        it('Should hide navigation', function () {

            menu.toggle(e);

            expect(toggleButton.hasClass('navigation-main-button--open')).to.be.false;
            expect(navigation.hasClass('navigation-toggle--open')).to.be.false;

        });

    });



    after(function () {
       $('.menu').remove();
    });
});


