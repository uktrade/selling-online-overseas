exports.config = {
    seleniumServerJar: '../../../node_modules/selenium-standalone-jar/bin/selenium-server-standalone-2.45.0.jar',

    capabilities: {
        'browserName': 'phantomjs',
        'phantomjs.binary.path':'./node_modules/karma-phantomjs-launcher/node_modules/phantomjs/bin/phantomjs',
        'phantomjs.ghostdriver.cli.args': ['--loglevel=DEBUG']
    },

    specs: ['./specs/*-spec.js'],

    jasmineNodeOpts: {
        showColors: true // Use colors in the command line report.
    }

};