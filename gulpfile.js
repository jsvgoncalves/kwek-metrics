var gulp = require('./gulp')([
    'bundle-css',
    'bundle-js'
]);

gulp.task('default', ['bundle-css']);

gulp.task('js', ['bundle-js']);

// Watch for SCSS changes
gulp.task('watch', function () {
  gulp.watch('./css/**/*.scss', ['bundle-css']);
});
