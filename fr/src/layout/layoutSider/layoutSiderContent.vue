<template>
  <n-layout-content position="absolute" style="top: 64px; bottom: 138px" :native-scrollbar="false">
    <n-menu :options="menuOptions" />
    
    
    
  </n-layout-content>
</template>

<script setup lang="ts">
import {type MenuOption} from "naive-ui";
import {setMenuOptions} from "../../tsFunc/latoutSider/layoutSiderContent.ts"
import {onMounted, ref} from "vue";


const menuOptions = ref<MenuOption[]>([])


onMounted(() => {
  menuOptions.value = setMenuOptions()
})


</script>

<style scoped>

</style>
