const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const isProd = process.env.NODE_ENV === 'production';
const extractSass = new ExtractTextPlugin({
	filename: "[name].[contenthash].css",
	disable: isProd
})
const cssDev = ['style-loader', 'css-loader', 'sass-loader'];
const cssProd = extractSass.extract({
	fallback: 'style-loader',
	use: ['css-loader', 'sass-loader']
});
const cssConfig = isProd ? cssProd : cssDev;


module.exports = {
	entry: {
		index: path.resolve(__dirname, 'client/index.jsx')
	},
	output: {
		path: path.resolve(__dirname, 'dist/'),
		filename: '[name]-[hash:12].js',
		publicPath: '/',
		chunkFilename: '[name]-[hash:12].js'
	},
	devServer: {
		hot: true,
		publicPath: '/',
		port: 9090,
		historyApiFallback: true,
		//open: true
		proxy: {
			'/api/*': {
				target: 'http://127.0.0.1:8080',
				changeOrigin: true
			}
		}
	},
	plugins: [
		new HtmlWebpackPlugin({
			template: './index.html',
			minify: {
		      collapseWhitespace: true,
		    },
		    hash: true
		}),
		new webpack.HotModuleReplacementPlugin(),
		new webpack.NamedModulesPlugin(),
		extractSass
	],
	module: {
		rules: [
			{
				test: /\.(jsx|js)$/,
				exclude: /node_modules/,
				use: {
					loader: 'babel-loader',
					options: {
						presets: ['react', 'es2015', 'stage-3']
					}
				}
			},
			{
				test: /\.scss$/,
				use: cssConfig
			},
			{
				test: /\.(png|jpg|gif)$/,
				loader: 'url-loader?limit=1000&name=./static/images/[name].[ext]?[hash]'
			}
		]	
	},
	resolve: {
		alias: {
			'@components': path.resolve(__dirname, 'client/components'),
			'@pages': path.resolve(__dirname, 'client/pages'),
			'@util': path.resolve(__dirname, 'client/util'),
		}
	}
}