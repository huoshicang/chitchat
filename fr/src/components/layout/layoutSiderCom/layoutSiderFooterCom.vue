<template>
  <n-flex vertical>
    <n-button ghost @click="New">
      新建
    </n-button>
    <n-button @click="active = true">设置</n-button>
    <n-button>关于</n-button>
  </n-flex>
  
  <n-drawer
    v-model:show="active"
    :default-width="isMobile ? 400 : 900"
    placement="right"
    resizable
  >
    <n-drawer-content>
      <n-alert title="注意保存" type="warning"></n-alert>
      <n-tabs type="line" default-tab="预设">
        <n-tab-pane name="模型" display-directive="show">
          <Model />
        </n-tab-pane>
        <n-tab-pane name="显示" display-directive="show">
          <Show />
        </n-tab-pane>
        <n-tab-pane name="预设" display-directive="show">
          <Prompts />
        </n-tab-pane>
      </n-tabs>
      
      </n-drawer-content>
  </n-drawer>

</template>

<script setup lang="ts">
import {onMounted, onUnmounted, ref, watch} from "vue";
import Model from "../../../components/drawer/model/index.vue"
import Show from "../../../components/drawer/show/index.vue"
import Prompts from "../../../components/drawer/prompts/index.vue"
import {info} from "../../../stores/info.ts";
import {useRoute} from "vue-router";
import {NButton} from "naive-ui";
import { useRouter } from 'vue-router';


const config = info();
const route = useRoute();
const router = useRouter();
const active = ref<boolean>(false)
const isMobile = ref(false);

const New = () => {
  router.push(`/`)
  config.set_title(null)
  config.set_new_chat(null)
  config.set_prompt(null)
}



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

// 监听路由变化
watch(
  [() => route.params.id, () => config.prompt],
  ([newId, newPrompt], [oldId, oldPrompt]) => {
    // 关闭弹窗
    if (!newId && newPrompt && newPrompt != oldPrompt) active.value = false
    
    
  },
  {immediate: true}
);


</script>

<style scoped>

</style>
