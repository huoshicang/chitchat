import { defineStore } from 'pinia'
import {reactive} from "vue";

export interface ModelValue {
  id: string | null
  name: string,
  model_var: {
    model: string,
    temperature: number | null,
    top_p: number | null
  },
  ai_var: {
    api_key: string,
    base_url: string
  },
  extra: Array
}

export const model = defineStore(
  'model',
  () => {

    // 模型值
    const modelValue = reactive<ModelValue>({
      name: "",
      model_var: {
        model: "",
        temperature: null,
        top_p: null
      },
      ai_var: {
        api_key: "",
        base_url: ""
      },
      extra: []
    })

    // 设置模型
    const setModel = (
      id: string | null,
      name: string,
      model_var: {
        model: string,
        emperature: number | null,
        top_p: number | null
      },
      ai_var: {
        api_key: string,
        base_url: string
      },
      extra: Array
      ) => {

      modelValue.id = id
      modelValue.name = name
      modelValue.model_var = model_var
      modelValue.ai_var = ai_var
      modelValue.extra = extra
    }

    return {
      modelValue,
      setModel
    }
  },
  {
    persist: {
      enabled: true,
      key: 'model',
      storage: localStorage,
    },
  }
)
