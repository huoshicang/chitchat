<template>
  <n-menu :options="menuOptions" :value="menuValue" @update:value="handleUpdateValue"/>
</template>

<script setup lang="ts">
import {type MenuOption, useMessage} from "naive-ui";
import {onMounted, ref, toRaw, watch} from "vue";
import {useRoute, useRouter} from 'vue-router';
import {setMenuOptions} from "./layoutSiderContent.data.ts";
import {info} from "../../../stores/info.ts";
import instance from "../../../api/fach.ts";

const config = info();
const msg = useMessage()
const route = useRoute();
const router = useRouter();

const menuOptions = ref<MenuOption[]>([])

const menuValue = ref<string | null>(null);

const handleUpdateValue = (key: string, item: MenuOption) => {
  router.push(`/chat/${key}`)
  config.set_title(item.label)
}

const getData = async () => {
  const {status_code, data, message} = await instance.get('chats/chat')
  if (status_code === 200) menuOptions.value = setMenuOptions(data)
  else msg.warning(message)
}

onMounted(async () => {
  await getData()
})

watch(
  [() => route.params.id, () => config.new_chat],
  ([newId, newChat], [oldId, ondChat]) => {
    // 修改选中值
    if (newId) menuValue.value = newId
    else menuValue.value = null
    
   
    
    if (newChat && newChat !== ondChat){
      menuOptions.value.push(setMenuOptions([toRaw(newChat)])[0])
    }
    
    
  },
  {
    immediate: true
  }
);

</script>

<style scoped>

</style>
