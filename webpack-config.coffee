# Commons Confing
module.exports =
  client:
    output:
      filename: './public/scripts/client.js'
    devtool: 'inline-source-map'
    resolve:
      extensions: ['', '.js', '.jsx']
    module:
      loaders: [
        {
          test: /\.js$|\.jsx$/
          exclude: /node_modules|src/
          loader: 'babel-loader?experimental&optional=selfContained'
        },
        {
          test: /\.jsx$/
          loader: 'jsx-loader?harmony'
        }
      ]