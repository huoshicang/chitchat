<template>
  <n-layout-content position="absolute" style="top: 64px; bottom: 138px" :native-scrollbar="false">
    <n-menu :options="menuOptions" :value="menuValue" @update:value="handleUpdateValue"/>
  </n-layout-content>
</template>

<script setup lang="ts">
import {type MenuOption, useMessage} from "naive-ui";
import {setMenuOptions} from "./layoutSiderContent.data.ts"
import {onMounted, ref, watch} from "vue";
import { useRoute, useRouter } from 'vue-router';
import instance from "../../../../api/fach.ts";
import {info} from "../../../../stores/info.ts";

const config = info();
const msg = useMessage()
const route = useRoute();
const router = useRouter();

const menuOptions = ref<MenuOption[]>([])

const menuValue = ref<string | null>(null);

const handleUpdateValue = (key: string, item: MenuOption) => {
  router.push(`/chat/${key}`)
  config.setTitle(item.title)
}

onMounted(async () => {
  const {status_code, data, message} = await instance.get('chats/chat')
  if (status_code === 200) menuOptions.value = setMenuOptions(data)
  else msg.warning(message)
})

watch(
  () => route.params.id,
  (newId) => {
    if (newId)  menuValue.value = newId
    else menuValue.value = null
  },
);

</script>

<style scoped>

</style>
