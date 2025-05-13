<template>
  <div class="flex flex-col">
    <div class="flex justify-between">
      <n-input-group class="input-group">
        <n-button ghost>
          <template #icon>
            <n-icon>
              <TrashOutline/>
            </n-icon>
          </template>
        </n-button>
      </n-input-group>
      <div class="w-69 flex justify-between">
        <ModelSelect/>
        <n-button ghost>
          <template #icon>
            <n-icon>
              <SendOutline/>
            </n-icon>
          </template>
        </n-button>
      </div>
      
    </div>
    <n-input
      v-model:value="value"
      type="textarea"
      placeholder="基本的 Textarea"
      :rows="4"
      round clearable show-count
    />
  </div>
</template>

<script setup lang="ts">
import ModelSelect from "../../components/drawer/model/select.vue"
import {SendOutline, TrashOutline} from "@vicons/ionicons5";
import {NButton, NIcon} from "naive-ui";
import {model} from "../../stores/model.ts";

const modelValue = model().modelValue
</script>

<style scoped>

</style>
