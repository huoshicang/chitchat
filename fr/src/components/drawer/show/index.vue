<template>
  <n-list hoverable clickable>
    
    <n-list-item>
      <n-thing title="信息">
        <template #description>
          <n-form
            label-placement="left"
            label-width="auto">
            <n-form-item label="setting_id">
              <n-input-group>
                <n-input :style="{ width: '60%' }" v-model:value="user_info.setting"/>
                <n-button type="primary" ghost @click="copyToClip(user_info.setting)">
                  复制
                </n-button>
              </n-input-group>
            </n-form-item>
            <n-form-item label="用户id">
              {{ user_info.user_id }}
            </n-form-item>
          </n-form>
        </template>
      </n-thing>
    </n-list-item>
    
    <n-list-item>
      <n-thing title="菜单">
        <template #description>
          <n-space size="large">
            <div>总开关：
              <n-switch v-model:value="sider_config.display"/>
            </div>
            <div>id：
              <n-switch v-model:value="sider_config.id"/>
            </div>
            <div>分享：
              <n-switch v-model:value="sider_config.share"/>
            </div>
            <div>归档：
              <n-switch v-model:value="sider_config.archive"/>
            </div>
          </n-space>
        </template>
      </n-thing>
    </n-list-item>
    <n-list-item>
      <n-thing title="消息">
        <template #description>
          <n-space size="large">
            <div>总开关：
              <n-switch v-model:value="message_config.show_all"/>
            </div>
            <div>模型：
              <n-switch v-model:value="message_config.show_model"/>
            </div>
            <div>提示令牌：
              <n-switch v-model:value="message_config.show_prompt_mark"/>
            </div>
            <div>完成令牌：
              <n-switch v-model:value="message_config.show_completion_token"/>
            </div>
            <div>总令牌：
              <n-switch v-model:value="message_config.show_token_total"/>
            </div>
            <div>推理令牌：
              <n-switch v-model:value="message_config.show_inference_token"/>
            </div>
            <div>时间：
              <n-switch v-model:value="message_config.show_time"/>
            </div>
            <div>思考：
              <n-switch v-model:value="message_config.think"/>
            </div>
          </n-space>
        </template>
      </n-thing>
    </n-list-item>
    <n-list-item>
      <n-thing title="预设">
        <template #description>
          <n-space size="large">
            <div>分享：
              <n-switch v-model:value="prompts_config.share"/>
            </div>
          </n-space>
        </template>
      </n-thing>
    </n-list-item>
    <n-list-item>
      <n-space justify="end">
        <n-button type="primary" @click="submit">
          确定
        </n-button>
      </n-space>
    </n-list-item>
  </n-list>

</template>

<script setup lang="ts">
import {settings} from "../../../stores/setting.ts"
import {useMessage} from "naive-ui"
import instance from "../../../api/fach.ts";
import {copyToClip} from "../../../utils/copy.ts";

const sider_config = settings().sider_config
const message_config = settings().message_config
const prompts_config = settings().prompts_config
const setting_cnfig = settings().setting_cnfig
const user_info = settings().user_info
const msg = useMessage()

// 复制
//const copyToClipboard = (text) => {
//  navigator.clipboard.writeText(text).then(() => {
//    msg.success('文本已复制到剪贴板');
//  }).catch(err => {
//    msg.error('无法复制文本: ', err);
//  });
//}

const submit = async () => {
  const {status_code, _, message} = await instance.post('/setting/edit', {
    setting: user_info.setting,
    id: user_info._id,
    sider_config,
    message_config,
    prompts_config
  })
  
  if (status_code === 200) msg.success('修改成功')
  else msg.error(message)
  
}

</script>

<style scoped>

</style>
