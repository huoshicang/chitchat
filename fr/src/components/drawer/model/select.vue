<template>
  <n-select style="width: 240px"
            v-model:value="ModelValue.modelValue.id"
            size="medium"
            :options="options"
            label-field="name"
            value-field="_id"
            @update:value="change"/>
</template>

<script setup lang="ts">
import {change} from "./index.data.ts";
import {watch, ref, onMounted} from "vue";
import instance from "../../../api/fach.ts";
import {model} from "../../../stores/model.ts";

const ModelValue = model()

const options = ref([])

const getData = async () => {
  const {status_code, data, message} = await instance.get("model/model")
  
  if (status_code === 200) options.value = data
  else {
    window.$message.warning(message)
    options.value = []
  }
}

onMounted(async () => await getData())

watch(() => ModelValue.modelValue.id, async (newValue) => {
  if (newValue === null) await getData()
  else if (newValue === ""){
    options.value.push(ModelValue.modelValue)
  }
})

</script>

<style scoped>

</style>
