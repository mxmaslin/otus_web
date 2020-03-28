const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin'); // Require  html-webpack-plugin plugin
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  entry: {
    'student_signup': __dirname + "/src/app/student-signup.js", // webpack entry point. Module to start building dependency graph
    'teacher_signup': __dirname + "/src/app/teacher-signup.js"
  },
  output: {
    path: __dirname + '/dist', // Folder to store generated bundle
    filename: '[name].js',  // Name of generated bundle after build
//    publicPath: '/' // public URL of the output directory when referenced in a browser
  },
  module: {  // where we defined file patterns and their loaders
      rules: [
      ]
  },
  plugins: [  // Array of plugins to apply to build chunk
      new HtmlWebpackPlugin({
          chunks: ['student_signup'],
          template: __dirname + "/profiles/templates/student-signup.html",
          filename: 'student-signup.html'
//          inject: 'body'
      }),
      new HtmlWebpackPlugin({
          chunks: ['teacher_signup'],
          template: __dirname + "/profiles/templates/teacher-signup.html",
          filename: 'teacher-signup.html'
//          inject: 'body'
      }),
      new BundleTracker({filename: './webpack-stats.json'})
  ],
//  devServer: {  // configuration for webpack-dev-server
//      contentBase: './src/public',  //source of static assets
//      port: 7700 // port to run dev-server
//  }
};