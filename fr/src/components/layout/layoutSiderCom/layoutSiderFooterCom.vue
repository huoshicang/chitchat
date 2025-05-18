<template>
  <n-flex vertical>
    <n-button @click="active = true">设置</n-button>
    <n-button>关于</n-button>
  </n-flex>
  
  <n-drawer
    v-model:show="active"
    :default-width="900"
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
import {ref, watch} from "vue";
import Model from "../../../components/drawer/model/index.vue"
import Show from "../../../components/drawer/show/index.vue"
import Prompts from "../../../components/drawer/prompts/index.vue"
import {info} from "../../../stores/info.ts";
import {useRoute} from "vue-router";

const config = info();
const route = useRoute();

const active = ref<boolean>(false)

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
