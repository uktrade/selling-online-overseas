describe('Mobile Navigation', function() {

    var toggleButton,
        navigation,
        e,
        html ='<div class="menu">' +
                '<a href="" class="header-nav-toggle" title="">menu</a>' +
                '<nav>' +
                    '<ul class="header-nav" style="display: none">' +
                        '<li class="header-nav-link"><a title="" href="" class="active">home</a></li>' +
                    '</ul>' +
                '</nav>' +
              '</div>';

    function init() {

        toggleButton = $('.header-nav-toggle'),
        navigation = $('.header-nav'),
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

            expect(toggleButton.hasClass('header-nav-toggle--open')).to.be.true;
            expect(navigation.hasClass('open')).to.be.true;

        });

        it('Should hide navigation', function () {

            menu.toggle(e);

            expect(toggleButton.hasClass('header-nav-toggle--open')).to.be.false;
            expect(navigation.hasClass('open')).to.be.false;

        });

    });



    after(function () {
       $('.menu').remove();
    });
});


