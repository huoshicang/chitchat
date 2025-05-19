<template>
  <layoutHeader/>
  <layoutCenter :messages="messages" :sendLoding="sendLoding"/>
  <layoutFooter @send_message="send_message" @clear_message="clear_message" :sendLoding="sendLoding"/>
</template>


<script setup lang="ts">
import layoutHeader from "../view/layout/layoutHeader.vue";
import layoutCenter from "../view/layout/layoutCenter.vue";
import layoutFooter from "../view/layout/layoutFooter.vue";
import {useMessage} from "naive-ui"
import {computed, ref, watch, toRaw} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import instance from "../api/fach.ts";
import {model} from "../stores/model.ts";
import {info} from "../stores/info.ts";

const msg = useMessage()
const route = useRoute();
const router = useRouter();
const config = info();
const chatId = ref<string | undefined>(route.params.id as string);
const ModelValue = model()
const messages = ref<[]>([]);
const sendLoding = ref<boolean>(false);

const messageListIndex = computed(() => {
  return messages.value.length - 1
})

let socket = null

/*
 * 发送消息
 * @param sendMessage 发送的消息
 * @return void
 * */
const send_message = (sendMessage: string) => {
  sendLoding.value = true;
  
  const host =
  import.meta.env.VITE_APP_WS_BALEURL !== "/chitchat/ws"
      ? import.meta.env.VITE_APP_BALEURL.replace(`${window.location.protocol}//`, "")
      : window.location.host;

  const protocol = window.location.protocol === "https:" ? "wss" : "ws";

  socket = new WebSocket(`${protocol}://${host}${import.meta.env.VITE_APP_WS_BALEURL}`,);
  
  let prompt = []
  
  if (messages.value[0]?.role === 'system') {
    prompt.push(messages.value[0])
  }
  
  prompt.push(
    {
      role: 'user',
      content: sendMessage
    }
  )
  
  // 发送数据
  const sendData = {
    authorization: localStorage.getItem("user_id"),
    message_id: route.params.id ?? "",
    message_index: messageListIndex.value,
    prompt: prompt,
    ai_var: toRaw(ModelValue.modelValue.ai_var),
    model_var: toRaw(ModelValue.modelValue.model_var),
    extra: toRaw(ModelValue.modelValue.extra)
  }
  
  //  连接成功
  socket.onopen = function () {
    
    // 添加消息到列表
    messages.value.push({
      content: sendMessage,
      role: "user",
    });
    
    // 发送初始消息或参数
    socket.send(JSON.stringify(sendData));
    
  };
  
  
  let is_one = true
  
  /*
   * 接收消息 拼接到最后一项
   * @param event 接收到的消息
   * @return void
   * */
  socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    
    const {status_code, message: data_message} = data;
    
    if (status_code !== 200) {
      messages.value.push(data);
      return;
    }
    
    // 跳转路由
    if (!data_message?.id) {
      config.set_title(data_message.title)
      config.set_new_chat(data_message)
      router.push(`/chat/${data_message.message_id}`)
      return;
    }
    
    if (is_one) {
      is_one = false;
      messages.value.push(data_message);
      return;
    }
    
    // 获取 choices
    const choices = data_message.choices?.[0] ?? {};
    // 获取 finish_reason
    const finish_reason = choices.finish_reason ?? "";
    // 获取 delta
    const delta = choices.delta ?? {};
    // 获取内容
    const reasoning_content = delta.reasoning_content ?? "";
    const content = delta.content ?? "";
    
    // 判断是否结束
    if (finish_reason !== "stop") {
      // 合并 delta 内容到当前消息
      const currentMessage = messages.value[messageListIndex.value].choices?.[0]?.delta || {};
      
      if (reasoning_content) {
        currentMessage.reasoning_content += reasoning_content;
      } else if (content) {
        currentMessage.content += content;
      }
    } else {
      // 替换最后一项
      const currentDelta = messages.value[messageListIndex.value].choices?.[0]?.delta || {};
      if (currentDelta.reasoning_content) {
        data_message.choices[0].delta.reasoning_content = currentDelta.reasoning_content;
      }
      if (currentDelta.content) {
        data_message.choices[0].delta.content = currentDelta.content;
      }
      
      messages.value[messageListIndex.value] = data_message;
    }
  };
  
  
  /*
   * 错误处理
   * @return void
   * */
  socket.onerror = function (error) {
    console.log(error)
  };
  
  /*
   * 关闭连接
   * @return void
   * */
  socket.onclose = function () {
    sendLoding.value = false;
    config.set_prompt(null)
  };
  
};


// 关闭连接
const clear_message = () => {
  socket.close()
  sendLoding.value = false;
}

// 获取数据
const getData = async () => {
  const {status_code, data, message} = await instance.get(`messages/${chatId.value}`)
  
  if (status_code === 200) {
    messages.value = data['message']
    if (data['message'].length == 0) await router.push(`/`)
  } else msg.warning(message)
}

// 监听路由变化
watch(
  [() => route.params.id, () => config.prompt],
  async ([newId, newPropt], [oldId, oldPropt]) => {
    
    // 清空数据逻辑
    if (!oldId && !newId) messages.value = []
    
    // 如果有新的消息 获取数据
    if (newId) {
      chatId.value = newId
      await getData()
    }
    
    if (newPropt) {
      messages.value.push({
        role: "system",
        content: newPropt,
      })
      chatId.value = null
    }
    
  },
  {immediate: true}
);

</script>


<style scoped>

</style>
