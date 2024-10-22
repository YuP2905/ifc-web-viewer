module.exports = {
  plugins: [
    "@babel/plugin-transform-class-static-block"
  ],
  presets: [
    '@vue/cli-plugin-babel/preset'
  ],
  // 忽略加快速度
  ignore: [
    'node_modules/three/**',
    'node_modules/@thatopen/components/**',
    'node_modules/web-ifc/**'
  ],
}
