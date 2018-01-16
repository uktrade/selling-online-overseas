var url = 'http://soo.trade.great:8008';

module.exports = {
    navigate: {
        home: url+'/',
        list: url+'/markets/results/'
    },
    pageHeader: element(by.css('h1.h1'))
};
