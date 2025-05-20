<template>
  <n-config-provider>
    <n-message-provider>
      <!--todo height在移动端有很大影响-->
      <n-layout class="h-screen" has-sider :style="{
        height: height + 'px',
      }"
      v-if="height !== null && width !== null">
        <layoutSider/>
        <n-layout >
          <router-view :key="$route.fullPath"/>
        </n-layout>
      </n-layout>
      <Config/>
    </n-message-provider>
  </n-config-provider>
</template>


<script setup lang="ts">
import layoutSider from "./view/layout/layoutSider.vue";
import Config from "./components/config.vue";
import {provide, onMounted, onUnmounted, ref} from "vue";
import {getFingerprint} from "./tsFunc/fingerprint.ts";
import {settings} from "./stores/setting.ts";

const Settings = settings()
const height = ref<number | null>(null)
const width = ref<number | null>(null)
const isMobile = ref<boolean | null>(null)

// 判断是否为移动设备的方法
const checkIsMobile = () => {
  const userAgent = navigator.userAgent || '';
  // 常见的移动端标识符
  const mobileKeywords = ['Android', 'webOS', 'iPhone', 'iPad', 'iPod', 'BlackBerry', 'Windows Phone'];
  
  // 检查 userAgent 是否包含任何一个关键字
  const isUserAgentMobile = mobileKeywords.some(keyword => userAgent.indexOf(keyword) > -1);
  
  height.value = window.innerHeight
  width.value = window.innerWidth
  isMobile.value = isUserAgentMobile || window.innerWidth <= 768
  
}


onUnmounted(() => {
  // 组件卸载时移除事件监听器
  window.removeEventListener('resize', checkIsMobile);
});

onMounted(async () => {
  
  checkIsMobile();
  // 监听窗口大小变化
  window.addEventListener('resize', checkIsMobile);
  
  if (!localStorage.getItem("user_id")) {
    const cachedFingerprint = await getFingerprint()
    localStorage.setItem("user_id", cachedFingerprint)
  }
  
  await Settings.getData()
  
  
});

provide('isMobile', isMobile)
provide('innerWidth', width)
provide('innerHeight', height)


</script>
