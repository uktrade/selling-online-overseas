describe('Autocomplete', function () {

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
            autoComplete.selectedEnter();

            expect($('.form-dropdown-tags li').length > 0).to.equal(true);
            expect($('.form-dropdown-tags li button').data('optionId')).to.equal('Health & Beauty');

            $('.form-dropdown-results, .form-dropdown-tags').empty();
        });

        it('One item selected press Enter', function () {
            init();

            $('.form-dropdown-results').append(result);
            $('.form-dropdown-results li').last().addClass('active');

            autoComplete.selectedEnter();

            expect($('.form-dropdown-tags li').length > 0).to.equal(true);
            expect($('.form-dropdown-tags li button').data('optionId')).to.equal('Cameras & Optics');

            $('.form-dropdown-results, .form-dropdown-tags').empty();
        });

        it('populates autocomplete  list', function () {

            var input = $('.form-dropdown-input'),
                data = {
                'suggestion': null,
                'categories': [
                    ['Health & Beauty', 'Medical Tests, Drugs Tests, HIV Tests, Pregnancy Tests,...'],
                    ['Business & Industrial', 'Test Tubes, Test Tube Racks'],
                    ['Hardware', 'Electrical Testing Tools, Electrical Testing Tool Accessories']],
                'query': 'test'
            },
            inputEvent;

            sinon.stub($, "ajax").callsFake( function(event) {
                var result = $.Deferred();
                result.args = event;
                return result;
            });

            autoComplete.inputEvent.call(input,event);

            inputEvent = $.ajax.getCall(0).returnValue;

            inputEvent.args;


            inputEvent.resolve(data);

            expect($('.form-dropdown-results li').length > 0).to.equal(true);

            expect($.ajax.calledOnce).to.be.true;

            $.ajax.restore();

        });

        it('close list', function () {
            dropdown.closeDropdown();
            expect($('.form-dropdown-results li').length).to.equal(0);

        });

    });

    describe('tags', function () {

        it('create a tag', function () {
           autoComplete.createTag($('ul.form-dropdown-tags'), 'product_categories', 'Health & Beauty',38319153556);
            expect($('.form-dropdown-tags li').length > 0).to.equal(true);
        });

        it('delete a tag', function () {

            var button = "<button data-button-id='38319153556' data-option-id='Health &amp; Beauty' data-item='product_categories' aria-label='close Health &amp; Beauty  tag' class='form-dropdown-tags--close'>x</button>";

            var event = $('button');

            autoComplete.deleteTag.call(event, {preventDefault: sinon.spy()})

            expect($('.form-dropdown-tags li').length).to.equal(0);
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