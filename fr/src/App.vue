<template>
  <n-layout class="h-screen" has-sider>
    <layoutSider/>
    <n-layout>
      <layoutHeader/>
      <layoutCenter/>
      <layoutFooter/>
    </n-layout>
  </n-layout>
</template>
<script setup lang="ts">
import layoutSider from "./layout/layoutSider.vue";
import layoutHeader from "./layout/layoutHeader.vue";
import layoutCenter from "./layout/layoutCenter.vue";
import layoutFooter from "./layout/layoutFooter.vue";
</script>
