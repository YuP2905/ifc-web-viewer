const { defineConfig } = require('@vue/cli-service');
const AutoImport = require('unplugin-auto-import/webpack').default;// 使用 default 导出
const Components = require('unplugin-vue-components/webpack').default; // 同样使用 default
const { ElementPlusResolver } = require('unplugin-vue-components/resolvers');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8082,
    // proxy: {
    //   '/uploads': {
    //     target: 'http://192.168.0.59:5000',
    //     changeOrigin: true,
    //   },
    //   }
  },

  configureWebpack: {
    plugins: [
      AutoImport({
        resolvers: [ElementPlusResolver()],
      }),
      Components({
        resolvers: [ElementPlusResolver()],
      }),
    ],
  },

  chainWebpack: config => {
    config.module
    .rule('js')
    .use('babel-loader')
    .tap(options => {

      options.plugins = [...(options.plugins || []), '@babel/plugin-transform-class-static-block'];
      return options;
    })
  }
  
});
