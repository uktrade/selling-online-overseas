exports.config = {
    seleniumServerJar: '../../../node_modules/selenium-standalone-jar/bin/selenium-server-standalone-3.0.1.jar',

    capabilities: {
        'browserName': 'chrome'
    },

    specs: ['./specs/*-spec.js'],

    jasmineNodeOpts: {
        showColors: true // Use colors in the command line report.
    }

};