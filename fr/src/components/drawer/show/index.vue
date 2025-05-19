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
              <n-switch v-model:value="siderContent.display"/>
            </div>
            <div>id：
              <n-switch v-model:value="siderContent.id"/>
            </div>
            <div>分享：
              <n-switch v-model:value="siderContent.share"/>
            </div>
            <div>归档：
              <n-switch v-model:value="siderContent.archive"/>
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
              <n-switch v-model:value="messageConfig.showAll"/>
            </div>
            <div>模型：
              <n-switch v-model:value="messageConfig.showModel"/>
            </div>
            <div>提示令牌：
              <n-switch v-model:value="messageConfig.showPromptTokens"/>
            </div>
            <div>完成令牌：
              <n-switch v-model:value="messageConfig.showCompletionTokens"/>
            </div>
            <div>总令牌：
              <n-switch v-model:value="messageConfig.showTotalTokens"/>
            </div>
            <div>推理令牌：
              <n-switch v-model:value="messageConfig.showReasoningTokens"/>
            </div>
            <div>时间：
              <n-switch v-model:value="messageConfig.showTime"/>
            </div>
            <div>思考：
              <n-switch v-model:value="messageConfig.think"/>
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
              <n-switch v-model:value="promptsConfig.share"/>
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

const siderContent = settings().siderContent
const messageConfig = settings().messageConfig
const promptsConfig = settings().promptsConfig
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
    siderContent,
    messageConfig,
    promptsConfig
  })
  
  if (status_code === 200) msg.success('修改成功')
  else msg.error(message)
  
}

</script>

<style scoped>

</style>
