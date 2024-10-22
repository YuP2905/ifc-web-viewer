const { defineConfig } = require('@vue/cli-service');
const AutoImport = require('unplugin-auto-import/webpack').default;// 使用 default 导出
const Components = require('unplugin-vue-components/webpack').default; // 同样使用 default
const { ElementPlusResolver } = require('unplugin-vue-components/resolvers');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8082,
    // proxy: {
    //   "/api" : {
    //     target: "https://api.vworld.kr",
    //     changeOrigin: true,
    //     pathRewrite: { "^/api": "" }
    //   },
      
    //   "/map": {
    //     target: "http://map2.daum.net",
    //     changeOrigin: true,
    //     pathRewrite: { "^/map": "/map/imageservice" }
    //   }
    // }
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

// import { defineConfig } from "@vue/cli-service";
// import AutoImport from 'unplugin-auto-import/vite'
// import Components from 'unplugin-vue-components/vite'
// import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// export default defineConfig({
//   transpileDependencies: true,
//   configureWebpack: {
//     plugins: [
//       AutoImport({
//         resolvers: [ElementPlusResolver()],
//       }),
//       Components({
//         resolvers: [ElementPlusResolver()],
//       })
//     ]
//   }
// })
