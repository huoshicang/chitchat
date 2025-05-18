<template>
  <n-page-header>
    <template #title>
      {{ title ?? "unnamed" }}
    </template>
  </n-page-header>
</template>
<script setup lang="ts">
import {info} from "../../stores/info.ts";
import {ref, watch} from "vue";

const title = ref("");

const config = info();


watch(
  () => config.title,
  (newValue) => {
    
    title.value = newValue
    
  },
  {immediate: true}
);


</script>

<style scoped>

</style>
