describe('result counts', function () {

    var html ='<form class="results-form">' +
                '<input checked="checked" id="id_product_categories_0" name="product_categories" type="checkbox" value="Accessories">' +
                '<input checked="checked" id="id_product_categories_0" name="product_categories" type="checkbox" value="books">' +
                '<div id="results-count" class="background--blue filters-container soft filters-result">' +
                    '<h4 class="results-count">1</h4>' +
                '</div>' +
              '</form>';



    it('Should update count result', function () {

        $('body').append(html);

        sinon.stub($, 'ajax').yieldsTo('success', {
            count: 2
        });

        resultCount.update_count();

        expect($.ajax.calledOnce).to.be.true;
        expect($('#results-count h4').text()).to.equal('2');

        $.ajax.restore();

        $('#results-form').remove();

    })

    after(function () {
        $('.results-form').remove();
    });

});