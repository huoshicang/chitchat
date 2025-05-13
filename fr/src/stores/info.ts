import { defineStore } from 'pinia'
import {ref} from "vue";


export const info = defineStore(
  'info',
  () => {

    const title = ref<string | null>(null)

    const setTitle = (value: string) => title.value = value

    return {
      title,
      setTitle
    }
  },
  {
    persist: {
      enabled: true,
      key: 'settings',
      storage: sessionStorage,
    },
  }
)
