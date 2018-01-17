module.exports = function (config) {
    'use strict';
    config.set({

        basePath: '',

        frameworks: ['mocha', 'chai', 'sinon'],

        files: [
            'node_modules/jquery/dist/jquery.js',
            'node_modules/underscore/underscore-min.js',
            'node_modules/slick-carousel/slick/slick.js',


            /* MOCHA */
            'app/assets/test/unit/**/*.spec.js',

            'app/assets/javascripts/**/*.js'
        ],

        preprocessors : {
            'app/assets/javascripts/**/*.js': 'coverage'
        },

        coverageReporter: {
            type : 'html',
            dir : 'app/assets/test/unit/coverage/'
        },

        // web server port
        port: 9876,

        // enable / disable colors in the output (reporters and logs)
        colors: true,

        // level of logging
        // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
        logLevel: config.LOG_INFO,

        // enable / disable watching file and executing tests whenever any file changes
        autoWatch: true,

        // start these browsers
        // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
        // browsers: ['Chrome', 'ChromeCanary', 'FirefoxAurora', 'Safari', 'PhantomJS'],
        browsers: ['ChromeHeadless'],

        // Continuous Integration mode
        // if true, Karma captures browsers, runs the tests and exits
        singleRun: true

    });
};
