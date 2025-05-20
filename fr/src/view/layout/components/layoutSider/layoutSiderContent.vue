<template>
  <n-layout-content position="absolute" :style="{
    bottom: '138px',
    height: height - 138 + 'px',
  }" :native-scrollbar="false">
    <layoutSiderContentCom/>
  </n-layout-content>
</template>

<script setup lang="ts">
import layoutSiderContentCom from "../../../../components/layout/layoutSiderCom/layoutSiderContentCom.vue"
import {inject} from "vue";

const height = inject('innerHeight')


</script>

<style scoped>

</style>
