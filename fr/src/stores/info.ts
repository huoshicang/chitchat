import {defineStore} from 'pinia'
import {ref} from "vue";


export const info = defineStore(
  'info',
  () => {

    const title = ref<null | string>(null)

    const new_chat = ref<{ket: string, value: string}>(null)

    const prompt = ref<null | string>(null)

    const set_title = (value: string | null) => title.value = value
    const set_new_chat = (value: {ket: string, value: string} | null) => new_chat.value = value
    const set_prompt = (value: string | null) => prompt.value = value

    return {
      title,
      set_title,
      new_chat,
      set_new_chat,
      prompt,
      set_prompt,
    }
  },
  {
    persist: {
      enabled: true,
      key: 'info',
      storage: sessionStorage,
    },
  }
)
