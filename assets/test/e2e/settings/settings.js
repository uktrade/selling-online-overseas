var url = process.env.TRAVIS ? 'http://ukti-navigator-staging.herokuapp.com' : 'http://localhost:8000';

module.exports = {
    navigate: {
        home: url+'/',
        list: url+'/markets/results/'
    },
    pageHeader: element(by.css('h1.h1'))
};
