var url = process.env.TRAVIS ? 'http://ukti-navigator-staging.herokuapp.com' : 'http://localhost:8000';

module.exports = {
    navigate: {
        home: url+'/markets/',
        filtering: url+'/markets/filter/',
        list: url+'/markets/search'
    },
    pageHeader: element(by.css('h1.heading-xlarge'))
};

/*TODO remove filter template not needed anymore */