/*
 * This file is part of Kwek Metrics.
 */

'use strict';

var gulp = require('gulp');
var gutil = require('gulp-util');
var sourcemaps = require('gulp-sourcemaps');
var browserify = require('browserify');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var uglify = require('gulp-uglify');
var babel = require('babelify');

module.exports = function () {
  // set up the browserify instance on a task basis
  var b = browserify({
    entries: './kwek-ui/app.js'
  }).transform("babelify", {
    "presets": ["es2015"]
  });

  return b.bundle()
    .pipe(source('app.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init({loadMaps: true}))
        // Add transformation tasks to the pipeline here.
        .pipe(uglify())
        .on('error', gutil.log)
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest('./static/js/'));
};
