gulp            = require 'gulp'
$               = do require 'gulp-load-plugins'
runSequence     = require 'run-sequence'
browserSync     = require 'browser-sync'
wpackconfig     = require './webpack-config.coffee'
source          = require 'vinyl-source-stream'
reload          = browserSync.reload

# Config
c =
  client    : 'client/'
  public    : './public/'
  src       : './src/'
  html      : 'html/'
  scripts   : 'scripts/'
  styles    : 'styles/'
  stylus    : 'stylus/'
  images    : 'images/'
  sprites   : 'sprites/'
  uglify    : true

###
Run Tasks
###

# run '$ gulp' : development(uglify:false)
gulp.task "default", [
  "watch"
  "images"
  "jade"
  "stylus"
  "script_livereload"
]

# run '$ gulp jade'
gulp.task "static", [
  "watch"
  "images"
  "jade"
  "stylus"
  "static_livereload"
]

# run '$ gulp build' : build only(uglify:true)
gulp.task "dev", [
  "images"
  "jade"
  "stylus"
  "webpack"
]



# Jade Build Live Reload
gulp.task "static_livereload", ->
  c.uglify = false
  runSequence ["webpack", "browsersync"]

# Watching
gulp.task "script_livereload", ->
  c.uglify = false
  runSequence ["webpack", "browsersync:proxy"]


# Watch
gulp.task "watch", ->

  $.watch [
    "#{c.src}#{c.scripts}**/*.js",
    "#{c.src}#{c.scripts}**/*.jsx"
  ], ->
    runSequence ["webpack"]

  $.watch ["#{c.src}#{c.html}*.jade", "#{c.src}#{c.html}**/*.jade"], ["jade"], ->
    runSequence ["jade"]


  $.watch ["#{c.src}#{c.styles}#{c.stylus}**/*.styl"], ["stylus"], ->
    runSequence ["stylus"]

# BrowserSync
gulp.task "browsersync:proxy", ->
  browserSync
    notify: false
    debugInfo: false
    open: false
    proxy: 'localhost:8000'
    port: '3000'

gulp.task "browsersync", ->
  browserSync
    server: './public'
    notify: false
    debugInfo: false
    open: false


# Webpack
# Configration
# '/webpack-config.coffee'
gulp.task "webpack", ->

  # Client
  gulp.src "#{c.src}#{c.scripts}app.js"
  .pipe $.webpack wpackconfig.client
  .pipe $.if c.uglify, do $.uglify
  .pipe browserSync.reload {stream: true}
  .pipe gulp.dest ""
  

# Stylus
gulp.task "stylus", ->

  gulp.src [
    "#{c.src}#{c.styles}#{c.stylus}!(_)**/!(_)*.styl"
  ]
  .pipe do $.stylus
  .pipe do $.pleeease
  .pipe $.minifyCss {keepSpecialComments: 0}
  .pipe $.rename {extname: ".css"}
  .pipe browserSync.reload {stream: true}
  .pipe gulp.dest "#{c.public}#{c.styles}"

# Jade
gulp.task "jade", ->
  gulp.src "#{c.src}#{c.html}!(_)*.jade"
  .pipe $.jade
    pretty: true
    basedir: "#{c.src}#{c.html}"
  .pipe browserSync.reload {stream: true}
  .pipe gulp.dest "#{c.public}"
  .on 'change', reload

# Images
gulp.task "images", ->
  gulp.src [
    "#{c.src}#{c.images}**/*.*"
    "#{c.src}#{c.images}!(#{c.sprite})/*.*"
  ]
  .pipe gulp.dest "#{c.public}#{c.images}"


# :Todo
###
- ダルいので使う時につくる
- Add WebFont Task
- Add Sprite Image Task
###



