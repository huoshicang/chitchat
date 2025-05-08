<template>
  <n-layout-content position="absolute" style="top: 64px; bottom: 138px" :native-scrollbar="false">
    <n-menu :options="menuOptions" />
    
    
    
  </n-layout-content>
</template>

<script setup lang="ts">
import {type MenuOption} from "naive-ui";
import {setMenuOptions} from "./layoutSiderContent.data.ts"
import {onMounted, ref} from "vue";


const menuOptions = ref<MenuOption[]>([])


onMounted(() => {
  menuOptions.value = setMenuOptions([
    {
      label: '首页',
      key: 'home',
      icon: 'home'
    },
  ])
})


</script>

<style scoped>

</style>
