describe('Filter', function() {

    var category, clickItem, activeTab, e, closeButton, form, filterFields,
        html ='<div class="filter">' +
                '<h1 class="heading-results"></h1>' +
                '<ul>' +
                    '<li><a href="#" class="filters-tab--item" data-group="product_categories"></a></li>' +
                    '<li><a href="#" class="filters-tab--item" data-group="product_categories__price"></a></li>' +
                '</ul>' +
                '<form class="filters-form">' +
                    '<div class="filters-options" data-field="product_categories" style="display: none">' +
                        '<input checked="checked" id="id_product_categories_0" name="product_categories" type="checkbox" value="Accessories">' +
                        '<input checked="checked" id="id_product_categories_0" name="product_categories" type="checkbox" value="books">' +
                    '</div>' +
                    '<div class="filters-options" data-field="product_categories__price" style="display: none">' +
                        '<input id="id_product_type_0" name="product_type" type="checkbox" value="Economy">' +
                        '<input id="id_product_type_0" name="product_type" type="checkbox" value="Luxury">' +
                    '</div>' +
                '</form>' +
              '</div>';

    function init(category) {
        category = category,
        clickItem = $('.filters-tab--item' + '[data-group="'+category+'"]'),
        activeTab = $('.filters-options' + '[data-field="'+category+'"]'),
        closeButton = $('.button-close'),
        form = $('.filters-form'),
        filterFields = $('.filters-form input'),
        e = {
            target : clickItem,
            preventDefault: sinon.spy(),
            data: {
                tabs: $('.filters-tab--item'),
                filters: $('.filters-options'),
                form: form
            }
        };
    }


    before(function() {
        $('body').append(html);
        init('product_categories');
    });

    describe('Click on the same tab', function () {

        it('Should activate clicked tab', function () {

            filter.toggle.call(clickItem, e);

            expect($(clickItem[0]).hasClass('active')).to.be.true;
            expect(activeTab.css('display')).to.equal('block');

        });

        it('Should deactivate clicked tab', function () {

            filter.toggle.call(clickItem, e);

            expect($(clickItem[0]).hasClass('active')).to.be.false;
            expect(activeTab.css('display')).to.equal('none');

        });
    });

    describe('Click on different tabs', function () {

        it('Should activate first tab', function () {

            filter.toggle.call(clickItem, e);

            expect($(clickItem[0]).hasClass('active')).to.be.true;
            expect(activeTab.css('display')).to.equal('block');

        });

        it('Should active second tab', function () {

            init('product_categories__price');

            filter.toggle.call(clickItem, e);

            expect($(clickItem[0]).hasClass('active')).to.be.true;
            expect(activeTab.css('display')).to.equal('block');

        });
    });

    describe('Click cancel button', function() {

        it('Should close the filter form', function () {


            filter.toggle.call(clickItem, e);

            filter.closeForm.call(closeButton, e);

            expect($(clickItem[0]).hasClass('active')).to.be.false;
            expect(activeTab.css('display')).to.equal('none');

        });
    });

    describe('Should update markets list', function () {

        it('Should make an api request to get filtered marketplace', function () {


            var deferred = new $.Deferred();
            deferred.resolve([{count:23}]);
            sinon.stub($, 'ajax').returns(deferred.promise());

            filter.updateMarketList.call(filterFields[2], e);

            expect($.ajax.calledTwice).to.be.true;
            $.ajax.restore();

        });
    });

    describe('Should update header', function () {

        it('Should update header 0 result', function () {
            expect(filter.setTitle(0)).to.equal('0 marketplace found');
        });

        it('Should update header 12 results', function () {
            expect(filter.setTitle(12)).to.equal('12 marketplaces found');
        });

    });



    after(function () {
       $('.filter').remove();
    });
});


