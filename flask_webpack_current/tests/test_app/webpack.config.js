var path = require('path')

var ExtractTextPlugin = require('extract-text-webpack-plugin')
var ManifestPlugin = require('webpack-manifest-plugin')

var rootAssetPath = './assets'

module.exports = {
	entry: {
		app_js: [
			rootAssetPath + '/scripts/entry.js'
		],
		app_css: [
			rootAssetPath + '/styles/main.css'
		]
	},
	output: {
		path: path.resolve(__dirname, './build/public'),
		filename: '[name].[chunkhash].js'
	},
	module: {
		rules: [
			{
        test: /\.css$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: 'css-loader'
        })
      },
      {
        test: /\.(gif|png|jpe?g|svg)$/i,
        use: [
          'file-loader',
          {
            loader: 'image-webpack-loader',
            options: {
              bypassOnDebug: true,
            },
          },
        ],
      }
		]
	},
	plugins: [
		new ExtractTextPlugin({
      filename: '[name].[chunkhash].css'
    }),
		new ManifestPlugin({
			fileName: 'manifest.json'
		})
	]
}
