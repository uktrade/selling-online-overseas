var url = 'http://localhost:' + process.env.PORT;

module.exports = {
    navigate: {
        home: url+'/markets/',
        filtering: url+'/markets/filter/',
        list: url+'/markets/search'
    },
    pageHeader: element(by.css('h1.h1'))
};
