module.exports = function (grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    compass: {
      options: {
        require: 'zurb-foundation',
        sassDir: 'app/static/sass',
        cssDir: 'app/static/stylesheets'
      },
      dev: {
      },
      production: {
        options: {
          environment: 'production',
          outputStyle: 'compressed',
          force: true
        }
      }
    },

    watch: {
      options: {
        livereload: true
      },
      styles: {
        files: ['app/static/sass/**/*.{sass,scss}'],
        tasks: ['compass:dev']
      }
    },

    imagemin: {
      all: {
        files: [{
          expand: true,
          cwd: 'app/static/img',
          src: ['**/*.{png,jpg,gif}'],
          dest: 'app/static/img'
        }]
      }
    }
  });

  require('load-grunt-tasks')(grunt);
  grunt.loadNpmTasks('grunt-contrib-imagemin');

  // Compiles SASS, assembles templates, starts dev server, watches for changes
  grunt.registerTask('default', ['compass:dev', 'watch']);
  // Build task builds minified versions of static files
  grunt.registerTask('build', ['compass:production', 'imagemin']);
};
