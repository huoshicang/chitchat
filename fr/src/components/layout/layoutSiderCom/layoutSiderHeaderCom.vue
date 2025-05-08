<template>
  <n-input-group class="h-15 flex items-center justify-center">
    <n-input autosize style="min-width: 50%" size="small" />
    <n-button ghost size="small">
     新建
    </n-button>
    <n-button ghost size="small">
      <template #icon>
        <n-icon>
          <TrashOutline/>
        </n-icon>
      </template>
    </n-button>
  </n-input-group>
</template>

<script setup lang="ts">

import {TrashOutline} from "@vicons/ionicons5";
import {NButton, NIcon} from "naive-ui";
</script>

<style scoped>

</style>
