<template>
  <n-form
    ref="formRef"
    :model="modelValue"
    :rules="rules"
    label-placement="left"
    label-width="auto"
    require-mark-placement="right-hanging"
    size="medium"
  >
    <n-card>
      <template #header>
        <ModelSelect/>
      </template>
      <template #header-extra>
        <n-button-group>
          <n-button ghost @click="copy">
            复制
          </n-button>
          <n-button ghost @click="del">
            删除
          </n-button>
        </n-button-group>
      </template>
      <n-form-item label="名称" path="name">
        <n-input v-model:value="modelValue.name"/>
      </n-form-item>
      <n-form-item label="key" path="api_key">
        <n-input type="password" show-password-on="click" v-model:value="modelValue.ai_var.api_key"/>
      </n-form-item>
      <n-form-item label="端点" path="base_url">
        <n-input v-model:value="modelValue.ai_var.base_url"/>
      </n-form-item>
      <n-form-item label="模型名" path="model">
        <n-input v-model:value="modelValue.model_var.model"/>
      </n-form-item>
      <n-form-item label="采样温度" path="temperature">
        <n-slider v-model:value="modelValue.model_var.temperature" :step="0.1" :max="1.9" :min="0"/>
      </n-form-item>
      <n-form-item label="采样率" path="top_p">
        <n-slider v-model:value="modelValue.model_var.top_p" :step="0.1" :max="1.0" :min="0"/>
      </n-form-item>
      <n-form-item label="额外参数">
        <n-dynamic-input
          v-model:value="modelValue.extra"
          preset="pair"
        />
      </n-form-item>
      
      <template #footer>
        <div style="display: flex; justify-content: flex-end">
          <n-button type="primary" attr-type="submit" @click="submit">
            提交
          </n-button>
        </div>
      </template>
    </n-card>
  </n-form>
</template>


<script setup lang="ts">
import ModelSelect from "./select.vue"
import {add, copy, del, edit, rules} from "./index.data.ts";
import {model} from "../../../stores/model.ts";
import {ref} from "vue";

const modelValue = model().modelValue
const formRef = ref(null)


const submit = (e: MouseEvent) => {
  formRef.value?.validate((errors) => {
    if (!errors) {
      if (modelValue.id) {
        edit(modelValue)
      } else {
        add(modelValue)
      }
    } else {
      console.log(errors)
      window.$message.error('验证失败')
    }
  })
}

</script>

<style scoped>

</style>
