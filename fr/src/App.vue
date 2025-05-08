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
import layoutSider from "./view/layout/layoutSider.vue";
import layoutHeader from "./view/layout/layoutHeader.vue";
import layoutCenter from "./view/layout/layoutCenter.vue";
import layoutFooter from "./view/layout/layoutFooter.vue";
import {onMounted} from "vue";
import instance from "./api/fach.ts";

onMounted(async () => {
  const {status_code, data, message} = await instance.get('/auth')
  console.log(status_code, data, message)
});


</script>
