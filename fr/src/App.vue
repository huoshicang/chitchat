<template>
  <n-config-provider>
    <n-message-provider>
      <n-layout class="h-screen" has-sider>
        <layoutSider/>
        <n-layout>
          <router-view :key="$route.fullPath" />
        </n-layout>
      </n-layout>
      <Config />
    </n-message-provider>
  </n-config-provider>
</template>


<script setup lang="ts">
import layoutSider from "./view/layout/layoutSider.vue";
import Config from "./components/config.vue";
import {onMounted} from "vue";
import {getFingerprint} from "./tsFunc/fingerprint.ts";
import {settings} from "./stores/setting.ts";

const Settings = settings()

onMounted(async () => {
  
  if (!localStorage.getItem("user_id")) {
    const cachedFingerprint = await getFingerprint()
    localStorage.setItem("user_id", cachedFingerprint)
  }
  
  await Settings.getData()
  
  
});
</script>
