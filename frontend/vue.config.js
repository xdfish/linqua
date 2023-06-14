const path = require("path");

module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  outputDir: path.resolve(__dirname, "../backend/server/server/www"),
  devServer: {
    proxy: 'http://localhost:8000'
  }
}
