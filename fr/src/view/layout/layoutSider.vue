<template>
  <n-layout-sider
    bordered
    :collapsed="isMobile"
    :native-scrollbar="false"
    :collapsed-width="0"
    :width="200"
    show-trigger="bar"
    @update:collapsed="isMobile = !isMobile">
    <layoutSiderContent/>
    <layoutSiderFooter/>
  </n-layout-sider>
</template>

<script setup lang="ts">
import layoutSiderContent from "./components/layoutSider/layoutSiderContent.vue"
import layoutSiderFooter from "./components/layoutSider/layoutSiderFooter.vue"
import {inject} from "vue";

const isMobile = inject('isMobile')




</script>

<style scoped lang="less">

.n-layout-footer {
  background-color: #00000000;
}

.but {
  color: red;
}

</style>
