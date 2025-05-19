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
import {onMounted, onUnmounted, ref} from "vue";

const isMobile = ref(false);

// 判断是否为移动设备的方法
function checkIsMobile() {
  const userAgent = navigator.userAgent || '';
  // 常见的移动端标识符
  const mobileKeywords = ['Android', 'webOS', 'iPhone', 'iPad', 'iPod', 'BlackBerry', 'Windows Phone'];
  
  // 检查 userAgent 是否包含任何一个关键字
  const isUserAgentMobile = mobileKeywords.some(keyword => userAgent.indexOf(keyword) > -1);
  
  // 结合视口宽度进行判断
  isMobile.value = isUserAgentMobile || window.innerWidth <= 768;
}

onMounted(() => {
  checkIsMobile();
  // 监听窗口大小变化
  window.addEventListener('resize', checkIsMobile);
});

onUnmounted(() => {
  // 组件卸载时移除事件监听器
  window.removeEventListener('resize', checkIsMobile);
});

</script>

<style scoped lang="less">

.n-layout-footer {
  background-color: #00000000;
}

.but {
  color: red;
}

</style>
