describe('Search', function () {

    var event, result, html = '<form class="form">' +
                '<label class="heading-small form-dropdown-header font-med flush--top" for="search-product">What kind of products do you sell? (optional)</label>'+
                '<input class="form-control form-dropdown-input column-one-whole" id="search-product" type="text" data-url="/products/api/" data-field="product_categories" autocomplete="off">'+
                '<ul class="form-dropdown-results" role="presentation"></ul>'+
                '<ul class="form-dropdown-tags"></ul>'+
                '<button class="button button-blue button-large push--top" type="submit">See results</button>'+
               '</form>';



    before(function() {
        $('body').append(html);

        /*TODO - need to revise */
        dataLayer = { push: function () {}};
    });

    function init() {
        result = '<li class="form-dropdown-list" role="option"><a href="" class="form-dropdown-option" data-option-id="Health &amp; Beauty"><b>Health &amp; Beauty</b> - First Aid, Hearing Aids, Incontinence Aids, Walking Aids,...</a></li>' +
            '<li class="form-dropdown-list" role="option"><a href="" class="form-dropdown-option" data-option-id="Home &amp; Garden"><b>Home &amp; Garden</b> - Rinse Aids</a></li>' +
            '<li class="form-dropdown-list" role="option"><a href="" class="form-dropdown-option" data-option-id="Animals &amp; Pet Supplies"><b>Animals &amp; Pet Supplies</b> - Pet Training Aids</a></li>' +
            '<li class="form-dropdown-list" role="option"><a href="" class="form-dropdown-option" data-option-id="Cameras &amp; Optics"><b>Cameras &amp; Optics</b> - Focusing Aids</a></li>',
        event = {
            target: $('.form-dropdown-input')
        };

    }


    describe('Autocomplete dropdown', function () {

        it('Press Enter to select first item', function () {
            init();

            $('.form-dropdown-results').append(result);
            search.selectedEnter();

            expect($('.form-dropdown-tags li').length > 0).to.equal(true);
            expect($('.form-dropdown-tags li button').data('optionId')).to.equal('Health & Beauty');

            $('.form-dropdown-results, .form-dropdown-tags').empty();
        });

        it('One item selected press Enter', function () {
            init();

            $('.form-dropdown-results').append(result);
            $('.form-dropdown-results li').last().addClass('active');

            search.selectedEnter();

            expect($('.form-dropdown-tags li').length > 0).to.equal(true);
            expect($('.form-dropdown-tags li button').data('optionId')).to.equal('Cameras & Optics');

            $('.form-dropdown-results, .form-dropdown-tags').empty();
        });

        xit('populates list', function () {

            var input = $('.form-dropdown-input');

            search.inputEvent.call(input,event);

            expect(true).to.equal(true);
        });

        xit('close list', function () {
            expect(true).to.equal(true);
        });

    });

    xdescribe('tags', function () {

        it('create a tag', function () {
            expect(true).to.equal(true);
        });

        it('delete a tag', function () {
            expect(true).to.equal(true);
        });

    });


    describe('search field', function () {

        it('clear field', function () {
            expect(true).to.equal(true);
        });


    });


    after(function () {
        //$('.form').remove();
    });

});