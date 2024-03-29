// GULPFILE
// - - - - - - - - - - - - - - -
// This file processes all of the assets in the "apps/assets" folder
// and outputs the finished files in the "staticfiles" folder.

// LIBRARIES
// - - - - - - - - - - - - - - -
import gulp from 'gulp';
import stylish from 'jshint-stylish';
import paths from './projectpath.babel';
import loadPlugins from 'gulp-load-plugins';
import karma from 'karma';

const plugins = loadPlugins(),
      Server = karma.Server;


// set debugMode to true to use non uglified and compressed js versions
let debugMode = false ? { mangle: false, compress: false, output: { beautify: true } } : null;

// TASKS
// - - - - - - - - - - - - - - -

gulp.task('javascripts', () => gulp
  .src([
    paths.src + 'javascripts/**/*.js'
  ])
  .pipe(plugins.babel({
    presets: ['es2015']
  }))
  .pipe(plugins.uglify(debugMode))
  .pipe(plugins.addSrc.prepend([
    paths.npm + 'jquery/dist/jquery.min.js',
    paths.npm + 'underscore/underscore-min.js',
    paths.npm + 'slick-carousel/slick/slick.js',
    paths.npm + 'query-command-supported/dist/queryCommandSupported.min.js',
    paths.npm + 'diff-dom/diffDOM.js'
  ]))
  .pipe(plugins.concat('all.js'))
  .pipe(gulp.dest(paths.dist + 'javascripts/'))
);

gulp.task('sass', () => gulp
  .src(paths.src + 'stylesheets/**/*.scss')
  .pipe(plugins.sass({
    outputStyle: 'compressed',
    includePaths: [
      paths.npm + 'govuk-elements-sass/public/sass/',
      paths.toolkit + 'stylesheets/',
      require("bourbon-neat").includePaths
    ]
  }))
  .pipe(plugins.base64({baseDir: 'apps'}))
  .pipe(gulp.dest(paths.dist + 'stylesheets/'))
);

// Watch for changes and re-run tasks
gulp.task('watchForChanges', function() {
  gulp.watch(paths.src + 'javascripts/**/*', ['javascripts', 'watch-unit-tests']);
  gulp.watch(paths.src + 'stylesheets/**/*.scss', ['sass']);
  gulp.watch(paths.src+ 'images/**/*', ['imagemin']);
  gulp.watch('gulpfile.babel.js', ['default']);
});

gulp.task('lint:sass', () => gulp
  .src([
    paths.src + 'stylesheets/**/*.scss',
    '!'+paths.src + 'stylesheets/admin/**/*.scss'
  ])
    .pipe(plugins.sassLint({
        rules: {
            'no-mergeable-selectors': 1, // Severity 1 (warning)
            'pseudo-element': 0,
            'no-ids': 0,
            'mixins-before-declarations': 0,
            'no-duplicate-properties': 0,
            'no-vendor-prefixes': 0,
            'clean-import-paths': 0
        }
    }))
    .pipe(plugins.sassLint.format())
    .pipe(plugins.sassLint.failOnError())
);

gulp.task('lint:js', () => gulp
  .src(paths.src + 'javascripts/**/*.js')
    .pipe(plugins.jshint({'esversion': 6, 'esnext': false}))
    .pipe(plugins.jshint.reporter(stylish))
    .pipe(plugins.jshint.reporter('fail'))
);

gulp.task('lint',
  ['lint:sass', 'lint:js']
);



gulp.task('unit-tests', () => {
    new Server({
        configFile: __dirname + '/karma.conf.js',
        reporters: ['progress', 'coverage']
    }).start();
});

gulp.task('watch-unit-tests', () => {
    new Server({
        configFile: __dirname + '/karma.conf.js',
        singleRun: false
    }).start();
});

// Default: compile everything
gulp.task('default',
  [
    'javascripts',
    'sass',
    'imagemin',
    'watch'
  ]
);

gulp.task('imagemin', () =>
    gulp.src(paths.src+'images/**/*')
        .pipe(plugins.imagemin({
            progressive: true
        }))
        .pipe(gulp.dest(paths.dist + 'images/'))
);

// Optional: recompile on changes
gulp.task('watch',
    ['watchForChanges']
);

gulp.task('test',
    [
     'lint',
     'unit-tests'
    ]
);

gulp.task('testfull',
    [
     'lint',
     'unit-tests',
    ]
);
