<template>
  <n-layout-sider bordered :native-scrollbar="false" :collapsed-width="0" :width="200" show-trigger="bar">
    
    <layoutSiderHeader/>
    <layoutSiderContent/>
    <layoutSiderFooter/>
  
  </n-layout-sider>
</template>

<script setup lang="ts">
import layoutSiderHeader from "./components/layoutSider/layoutSiderHeader.vue"
import layoutSiderContent from "./components/layoutSider/layoutSiderContent.vue"
import layoutSiderFooter from "./components/layoutSider/layoutSiderFooter.vue"


</script>

<style scoped lang="less">

.n-layout-footer {
  background-color: #00000000;
}

.but {
  color: red;
}

</style>
