<template>
  <n-input-group class="h-15 flex items-center justify-center">
    <n-button ghost @click="New">
     新建
    </n-button>
    <n-button ghost>
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
import { useRouter } from 'vue-router';
import {info} from "../../../stores/info.ts";
const config = info();

const router = useRouter();

const New = () => {
  router.push(`/`)
  config.setTitle(null)
}

</script>

<style scoped>

</style>
