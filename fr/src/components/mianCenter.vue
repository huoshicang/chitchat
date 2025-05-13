<template>
  <layoutHeader/>
  <layoutCenter :messages="messages"/>
  <layoutFooter/>
</template>


<script setup lang="ts">
import layoutHeader from "../view/layout/layoutHeader.vue";
import layoutCenter from "../view/layout/layoutCenter.vue";
import layoutFooter from "../view/layout/layoutFooter.vue";
import {useMessage} from "naive-ui"
import {ref, watch} from 'vue';
import {useRoute} from 'vue-router';
import instance from "../api/fach.ts";

const msg = useMessage()
const route = useRoute();
const chatId = ref<string | undefined>(route.params.id as string);

const messages = ref<[]>([]);

// 获取数据
const getData = async () => {
  const {status_code, data, message} = await instance.get(`messages/${chatId.value}`)
  
  if (status_code === 200) {
    messages.value = data['message']
  } else msg.warning(message)
}

// 监听路由变化
watch(
  () => route.params.id,
  async (newId) => {
    
    if (newId) {
      chatId.value = newId
      await getData()
    }
  },
  {immediate: true}
);

</script>


<style scoped>

</style>
