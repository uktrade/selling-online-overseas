describe('result counts', function () {

    var html ='<form="results-form">' +
                '<input checked="checked" id="id_product_categories_0" name="product_categories" type="checkbox" value="Accessories">' +
                '<input checked="checked" id="id_product_categories_0" name="product_categories" type="checkbox" value="books">' +
                '<div id="results-count" class="background--blue filters-container soft filters-result">' +
                    '<h5>1</h5>' +
                '</div>' +
              '</form>';



    it('Should update count result', function () {

        $('body').append(html);

        sinon.stub($, 'ajax').yieldsTo('success', {
            count: 2
        });

        resultCount.update_count();

        expect($.ajax.calledOnce).to.be.true;
        expect($('#results-count h5').text()).to.equal('2');

        $.ajax.restore();

        $('#results-form').remove();

    })

});