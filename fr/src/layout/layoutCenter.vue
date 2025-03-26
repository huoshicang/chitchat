<template>
  <n-layout-content position="absolute" style="top: 64px; bottom: 140px" content-style="padding: 24px;"
                    :native-scrollbar="false">
    <n-infinite-scroll :distance="10">
      <div
        v-for="(item, index) in messages"
        :key="index"
        class="message"
        :class="{ reverse: item.role === 'user' }"
      >
        <img class="avatar" src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg" alt="">
        <div>
          <span>{{ item.content }}</span>
          <n-input-group class="input-group">
            <n-button ghost>
              <template #icon>
                <n-icon>
                  <ChatbubblesOutline/>
                </n-icon>
              </template>
            </n-button>
            <n-button ghost>
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

const messages = []

</script>

<style scoped>
.message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
  padding: 10px;
  margin-right: 50px;
  
  &:hover .input-group {
    opacity: 1;
  }
  
  .input-group {
    opacity: 0;
  }
  
  &:last-child {
    margin-bottom: 0;
  }
  
  .avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    margin-right: 10px;
  }
  
}

.reverse {
  flex-direction: row-reverse;
  margin-left: 50px;
  margin-right: 0;
  
  .avatar {
    margin-left: 10px;
  }
}


</style>
