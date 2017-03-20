/*
 * This file is part of Kwek Metrics.
 */

const { mix } = require('laravel-mix');

mix.js('js/index.js', 'static/js')
   .sass('css/style.scss', 'static/css');
