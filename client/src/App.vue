<template>
<IfcViewer />
</template>

<script>
import IfcViewer from "./components/IfcViewer.vue"

export default {
  name: "App",
  components: {
    IfcViewer,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}
</style>
