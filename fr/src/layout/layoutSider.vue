<template>
  <n-layout-sider bordered :native-scrollbar="false" :collapsed-width="0" :width="200" show-trigger="bar">
    
    <layoutSiderHeader/>
    <layoutSiderContent/>
    <layoutSiderFooter/>
  
  </n-layout-sider>
</template>

<script setup lang="ts">
import layoutSiderHeader from "./layoutSider/layoutSiderHeader.vue"
import layoutSiderContent from "./layoutSider/layoutSiderContent.vue"
import layoutSiderFooter from "./layoutSider/layoutSiderFooter.vue"


</script>

<style scoped lang="less">

.n-layout-footer {
  background-color: #00000000;
}

.but {
  color: red;
}

</style>
