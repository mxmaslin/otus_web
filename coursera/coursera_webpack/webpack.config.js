const webpack = require('webpack');
const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist'),
  },
  module: {
      rules: [
        {
            test: /\.css$/i,
            use: [MiniCssExtractPlugin.loader, 'css-loader']
         }
      ],
  },
  plugins: [
      new BundleTracker({filename: './webpack-stats.json'}),
      new MiniCssExtractPlugin()
  ],
//  devServer: {  // configuration for webpack-dev-server
//      contentBase: './src/public',  //source of static assets
//      port: 7700 // port to run dev-server
//  }
};