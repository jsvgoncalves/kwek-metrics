var gulp = require('./gulp')([
    'bundle-css'
]);

gulp.task('default', ['bundle-css']);

// Watch for SCSS changes
gulp.task('watch', function () {
  gulp.watch('./css/**/*.scss', ['bundle-css']);
});
