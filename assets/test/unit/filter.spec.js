describe('Filter', function() {

    var category, clickItem, activeTab, e, closeButton,
        html ='<div class="filter">' +
                '<ul>' +
                    '<li><a href="#" class="filters-tab--item" data-group="product_categories"></a></li>' +
                    '<li><a href="#" class="filters-tab--item" data-group="product_categories__price"></a></li>' +
                '</ul>' +
                '<form>' +
                    '<div class="filters-options" data-field="product_categories" style="display: none">' +
                        '<input checked="checked" id="id_product_categories_0" name="product_categories" type="checkbox" value="Accessories"></div>' +
                        '<input checked="checked" id="id_product_categories_0" name="product_categories" type="checkbox" value="books"></div>' +
                    '<div class="filters-options" data-field="product_categories__price" style="display: none"></div>' +
                '</form>' +
              '</div>';

    function init(category) {
        category = category,
        clickItem = $('.filters-tab--item' + '[data-group="'+category+'"]'),
        activeTab = $('.filters-options' + '[data-field="'+category+'"]'),
        closeButton = $('.button-close'),
        e = {
            target : clickItem,
            preventDefault: sinon.spy(),
            data: {
                tabs: $('.filters-tab--item'),
                filters: $('.filters-options')
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


    after(function () {
       $('.filter').remove();
    });
});


