<template>
  <n-layout-footer position="absolute" class="h-34.5">
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
          <n-button v-show="!props.sendLoding" ghost @click="sendMessageFooter" :loading="props.sendLoding" :disabled="props.sendLoding">
            <template #icon>
              <n-icon>
                <SendOutline/>
              </n-icon>
            </template>
          </n-button>
          <n-button v-show="props.sendLoding" @click="emit('clear_message')" ghost>
            <template #icon>
              <n-icon>
                <StopCircleOutline/>
              </n-icon>
            </template>
          </n-button>
        </div>
      
      </div>
      <n-input
        v-model:value="text"
        
        type="textarea"
        placeholder=""
        :rows="4"
        round clearable show-count
      />
    </div>
  </n-layout-footer>
</template>

<script setup lang="ts">
import {NButton, NIcon, useMessage} from "naive-ui";
import ModelSelect from "../../components/drawer/model/select.vue";
import {SendOutline, TrashOutline, StopCircleOutline} from "@vicons/ionicons5";
import {ref} from "vue";

const message = useMessage()

const props = defineProps({
  sendLoding: {
    type: Boolean,
    required: false,
  },
});

// 输入框文本
const text = ref<string>("");

// 父组件触发事件 发送消息
const emit = defineEmits(["send_message", "clear_message"]);

// 发送消息
const sendMessageFooter = () => {
  if (text.value === "") {
    message.warning("请输入内容")
    return;
  }
  
  
  emit("send_message", text.value);
  text.value = "";
};

</script>

<style scoped>
.n-layout-footer {
  background-color: #00000000;
}
</style>
