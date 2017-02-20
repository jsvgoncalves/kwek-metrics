'use strict';

var gulp      = require('gulp');
var sourcemaps = require('gulp-sourcemaps');
var sass = require('gulp-sass');
var minifyCss = require('gulp-minify-css');

module.exports = function() {
  return gulp.src('./css/**/*.scss')
   .pipe(sourcemaps.init())
   .pipe(sass.sync().on('error', sass.logError))
   .pipe(minifyCss())
   .pipe(sourcemaps.write('./maps'))
   .pipe(gulp.dest('./static/css'));
};
