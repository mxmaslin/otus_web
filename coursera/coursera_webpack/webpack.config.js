const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  entry: {
    'student_signup': __dirname + "/assets/entries/student-signup.html",
    'teacher_signup': __dirname + "/assets/entries/teacher-signup.html"
  },
  output: {
    path: __dirname + '/assets/bundles',
//    filename: '[name]-[hash].js',
//    publicPath: '/' // public URL of the output directory when referenced in a browser
  },
  module: {  // where we defined file patterns and their loaders
      rules: [
        {
            include: __dirname + '/assets/'
        }
      ],
  },
  plugins: [
      new HtmlWebpackPlugin({
          chunks: ['student_signup'],
          template: __dirname + "/profiles/templates/student-signup.html",
          filename: 'student-signup-[hash].html'
//          inject: 'body'
      }),
      new HtmlWebpackPlugin({
          chunks: ['teacher_signup'],
          template: __dirname + "/profiles/templates/teacher-signup.html",
          filename: 'teacher-signup-[hash].html'
//          inject: 'body'
      }),
      new BundleTracker({filename: './webpack-stats.json'})
  ],
//  devServer: {  // configuration for webpack-dev-server
//      contentBase: './src/public',  //source of static assets
//      port: 7700 // port to run dev-server
//  }
};