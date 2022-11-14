const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
      proxy: {
          '/api/v1': {
              target: 'http://127.0.0.1:8001',
              pathRewrite: { '^/api/v1': '' }
         },
     }
 }

})
