var url = 'http://localhost:' + process.env.PORT;

module.exports = {
    navigate: {
        home: url+'/',
        list: url+'/markets/results/'
    },
    pageHeader: element(by.css('h1.h1'))
};
