import {defineStore} from 'pinia'
import {ref} from "vue";
import instance from "../api/fach.ts";


export const settings = defineStore(
  'settings',
  () => {

    const user_info: { [key: string]: boolean } | null = ref(null)

    const siderContent: { [key: string]: boolean } = ref()

    const messageConfig: { [key: string]: boolean } = ref()

    const getData = async () => {
      const {status_code, data, message} = await instance.get('/auth')

      user_info.value = {
        setting: data.setting,
        user_id: data.user_id,
        _id: data._id,
      }

      siderContent.value = data.siderContent
      messageConfig.value = data.messageConfig
    }

    return {
      user_info,
      siderContent,
      messageConfig,
      getData,
    }
  },
  {
    persist: {
      enabled: true,
      key: 'settings',
      storage: localStorage,
    },
  }
)
