exports.config = {
    seleniumServerJar: '../../../node_modules/selenium-standalone-jar/bin/selenium-server-standalone-3.0.1.jar',

    capabilities: {
        'browserName': 'chrome'
    },

    debug: false,

    autoStartStopServer: true,

    jasmineNodeOpts: {
        showColors: true // Use colors in the command line report.
    }

};