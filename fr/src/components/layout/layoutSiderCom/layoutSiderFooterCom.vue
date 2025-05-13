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
      <n-tabs type="line">
        <n-tab-pane name="模型" display-directive="show">
          <Model />
        </n-tab-pane>
        <n-tab-pane name="显示" display-directive="show">
          <Show />
        </n-tab-pane>
        <n-tab-pane name="预设" display-directive="show">
          在两点半消失
        </n-tab-pane>
      </n-tabs>
      
      </n-drawer-content>
  </n-drawer>

</template>

<script setup lang="ts">
import {ref} from "vue";
import Model from "../../../components/drawer/model/index.vue"
import Show from "../../../components/drawer/show/index.vue"

const active = ref<boolean>(true)

</script>

<style scoped>

</style>
