import {defineStore} from 'pinia'
import {ref} from "vue";
import {Api} from "../api/api.ts";


export const settings = defineStore(
  'settings',
  () => {

    const user_info: { [key: string]: boolean } | null = ref(null)

    const sider_config: { [key: string]: boolean } = ref()

    const message_config: { [key: string]: boolean } = ref()

    const prompts_config: { [key: string]: boolean } = ref()

    const setting_cnfig: { [key: string]: boolean } = ref()

    const getData = async () => {
      const {status_code, data, message} = await Api.auth()

      user_info.value = {
        setting: data.setting,
        user_id: data.user_id,
        _id: data._id,
      }

      sider_config.value = data.sider_config
      message_config.value = data.message_config
      prompts_config.value = data.prompts_config
      setting_cnfig.value = data.setting_cnfig


    }

    return {
      user_info,
      sider_config,
      message_config,
      prompts_config,
      setting_cnfig,
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
