<template>
  <n-form
    ref="formRef"
    :model="props.new_prompt"
    :rules="rules"
    label-placement="left"
    label-width="auto"
    require-mark-placement="right-hanging">
    <n-form-item label="标题" path="title">
      <n-input v-model:value="props.new_prompt.title" placeholder=""/>
    </n-form-item>
    <n-form-item label="提示" path="prompt">
      <n-input  type="textarea" :autosize="{
        minRows: 3,
      }" v-model:value="props.new_prompt.prompt" placeholder=""/>
    </n-form-item>
    
    <div style="display: flex; justify-content: flex-end">
      <n-button type="primary" @click="submit">
        提交
      </n-button>
    </div>
  </n-form>
</template>

<script setup lang="ts">
import {add, edit, rules} from "./index.data.ts";
import {ref} from "vue";

const formRef = ref(null)

const props = defineProps({
  new_prompt: {
    type: Object,
    default: {
      _id: '',
      title: '',
      prompt: '',
    }, // 未传值时的默认值
  },
});


const submit = (e: MouseEvent) => {
  formRef.value?.validate((errors) => {
    if (!errors) {
      
      if (props.new_prompt._id) {
        props.new_prompt['id'] = props.new_prompt._id
        edit(props.new_prompt)
      } else {
        add(props.new_prompt)
      }
    } else {
      window.$message.error('验证失败')
    }
  })
}

</script>

<style scoped>

</style>
