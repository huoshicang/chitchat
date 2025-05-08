<template>
  <n-layout-content position="absolute" style="top: 64px; bottom: 140px" content-style="padding: 24px;"
                    :native-scrollbar="false">
    <n-infinite-scroll :distance="10">
      <div
        v-for="(item, index) in messages"
        :key="index"
        class="message flex mb-2.5"
        :class="item.role === 'user' ? 'flex-row-reverse ml-12.5 mr-0' : 'ml-0 mr-12.5'"
      >
        <img class="w-7 h-7 rounded-full" :class="item.role === 'user' ? 'ml-2' : 'mr-2'" src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg" alt="">
        <div class="flex flex-col" :class="item.role === 'user' ? 'items-end' : 'items-start'">
          <span>{{ item.content }}</span>
          <n-input-group class="input-group">
            <n-button ghost size="small">
              <template #icon>
                <n-icon>
                  <ChatbubblesOutline/>
                </n-icon>
              </template>
            </n-button>
            <n-button ghost size="small">
              <template #icon>
                <n-icon>
                  <TrashOutline/>
                </n-icon>
              </template>
            </n-button>
          </n-input-group>
        </div>
      
      
      </div>
    </n-infinite-scroll>
  </n-layout-content>
</template>

<script setup lang="ts">

import {NButton, NIcon} from "naive-ui";
import {ChatbubblesOutline, TrashOutline} from "@vicons/ionicons5";

const messages = [
  {
    role: 'user',
    content: '你好',
  },
  {
    role: 'assistant',
    content: '你好',
  },
]

</script>

<style scoped>
.message {
  
  &:hover .input-group {
    opacity: 1;
  }
  
  .input-group {
    opacity: 0;
  }
  
  &:last-child {
    margin-bottom: 0;
  }
  
}


</style>
