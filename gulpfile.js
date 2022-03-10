const {src, dest, series, parallel, watch, task} = require('gulp');

const concat = require('gulp-concat');
const cssNano = require('gulp-csso');
const rename = require('gulp-rename');
const uglify = require('gulp-uglify-es').default;
const autoprefixer = require('gulp-autoprefixer');
const browserSync = require('browser-sync');
const child_process = require('child_process');

task('runserver', function (cb) {
    const runserver = child_process.exec('python src/manage.py runserver');

    runserver.on('close', function (code) {
        if (code !== 0) {
            console.error('Django runserver exited with error code: ' + code);
        } else {
            console.log('Django runserver exited normally.');
        }
    });

    cb();
});

task('browsersync', function (cb) {
    browserSync.init({
        proxy: 'localhost:8000',
        port: 8000,
        online: true,
    });

    cb();
});


function styles() {
    return src('src/static/css/style.css')
        .pipe(concat('style.min.css'))
        .pipe(autoprefixer({
            overrideBrowserslist: ['last 10 versions'],
            grid: true,
        }))
        .pipe(cssNano({
            restructure: false,
            sourceMap: true,
            debug: true,
        }))
        .pipe(dest('src/static/css/'))
        .pipe(browserSync.stream());
}

function scripts() {
    return src(['node_modules/axios/dist/axios.js',
        'node_modules/vue/dist/vue.global.js',
        'src/static/js/app.js',
        'src/static/js/vueApp.js'])
        .pipe(concat('app.min.js'))
        .pipe(uglify())
        .pipe(dest('src/static/js/app/'))
        .pipe(browserSync.stream());
}

function startWatch() {
    watch(['src/static/js/**/*.js', '!src/static/js/app/*.min.js'], scripts);
    watch(['src/static/css/**/*.css', '!src/static/css/**/*.min.css'], styles);
    watch('src/templates/**/*.html').on('change', browserSync.reload);
    watch(['src/**/*.py', '!src/static/', '!src/media/']).on('change', browserSync.reload);
}

exports.styles = styles;
exports.scripts = scripts;
exports.build = parallel(scripts, styles);
exports.default = parallel(scripts, styles, series(task('runserver'), task('browsersync')), startWatch);