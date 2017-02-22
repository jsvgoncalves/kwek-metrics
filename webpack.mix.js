/*
 * This file is part of Kwek Metrics.
 */

const { mix } = require('laravel-mix');

mix.js('kwek-ui/app.js', 'static/js')
   .sass('css/style.scss', 'static/css');
