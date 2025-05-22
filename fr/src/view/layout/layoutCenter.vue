<template>
  <n-layout-content position="absolute" :style="{
  top: '64px',
  bottom: '140px',
  height: isHeight / 16 - 12.375 + 'rem',
  }" content-style="padding: 24px;"
                    :native-scrollbar="false">
    <n-infinite-scroll :distance="10">
      <div
        v-for="(item, index) in props.messages"
        :key="index"
        class="message flex mb-2.5"
        :class="item.role === 'user' ? 'flex-row-reverse ml-12.5 mr-0' : 'ml-0 mr-12.5'"
      >
        
        <!--头像-->
        <n-avatar
          class="w-7 h-7 rounded-full" :class="item.role === 'user' ? 'ml-2' : 'mr-2'"
          round
          size="medium"
          :style="{ backgroundColor: 'rgb(255 255 255 / 0%)', }"
          :src="item.role === 'user' ? 'https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg' : ''"
        >
          <n-icon v-if="item.id">
            <svg t="1747639213398" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1484" xmlns:xlink="http://www.w3.org/1999/xlink" width="200" height="200">
              <path d="M256 469.333333a85.333333 85.333333 0 0 1 85.333333-85.333333h341.333334a85.333333 85.333333 0 0 1 85.333333 85.333333v298.666667a85.333333 85.333333 0 0 1-85.333333 85.333333H341.333333a85.333333 85.333333 0 0 1-85.333333-85.333333z m256-384a85.333333 85.333333 0 0 0-85.333333 85.333334 85.333333 85.333333 0 0 0 42.666666 73.386666V298.666667H341.333333a170.666667 170.666667 0 0 0-170.666666 170.666666v85.333334a85.333333 85.333333 0 0 0 0 170.666666v42.666667a170.666667 170.666667 0 0 0 170.666666 170.666667h341.333334a170.666667 170.666667 0 0 0 170.666666-170.666667v-42.666667a85.333333 85.333333 0 0 0 0-170.666666v-85.333334a170.666667 170.666667 0 0 0-170.666666-170.666666h-128V244.053333a85.333333 85.333333 0 0 0-24.32-156.586666A67.413333 67.413333 0 0 0 512 85.333333z m-42.666667 448a64 64 0 0 0-128 0 21.333333 21.333333 0 0 0 21.333334 21.333334h85.333333a21.333333 21.333333 0 0 0 21.333333-21.333334z m149.333334-64a64 64 0 0 0-64 64 21.333333 21.333333 0 0 0 21.333333 21.333334h85.333333a21.333333 21.333333 0 0 0 21.333334-21.333334 64 64 0 0 0-64-64z m-21.333334 170.666667h-170.666666a42.666667 42.666667 0 0 0-42.666667 42.666667 85.333333 85.333333 0 0 0 85.333333 85.333333h85.333334a85.333333 85.333333 0 0 0 85.333333-85.333333 42.666667 42.666667 0 0 0-42.666667-42.666667z" p-id="1485" fill="#8a8a8a"></path>
            </svg>
          </n-icon>
        </n-avatar>
        
        <div class=" flex flex-col" :class="item.role === 'user' ? 'items-end' : 'items-start'">
          
          <n-space>
            <!--思考-->
            <n-collapse arrow-placement="right" class="ml-3" v-show="reasoning_content_show(item)">
              <n-collapse-item title="思考">
                <Text :text="reasoning_content(item)"/>
              </n-collapse-item>
            </n-collapse>
            <!--system内容-->
            <n-ellipsis v-if="item.role === 'system'" expand-trigger="click" line-clamp="2" :tooltip="false">
              {{ item.content }}
            </n-ellipsis>
            <!--消息内容-->
            <Text  v-else :error="item.status_code" :asRawText="item.status_code" :text="content(item)"/>
            <n-spin size="small" v-show="index === props.messages.length - 1 && sendLoding && item.id" />
          </n-space>
          
          <!--额外信息-->
          <div v-show="item.role !== 'user' && item.role !== 'system' && config.show_all">
            <n-text depth="3" class="ml-3"> {{ generateDisplay(item) }}
              <span v-show="config.show_time && item.created">
                 | <n-time :time="item.created" unix/>
              </span>
            </n-text>
          </div>
          <!--操作按钮-->
          <n-input-group class="input-group">
            <!--编辑-->
            <n-button ghost size="small" disabled>
              <template #icon>
                <n-icon>
                  <Pencil/>
                </n-icon>
              </template>
            </n-button>
            <!--复制-->
            <n-button ghost size="small" @click="copyToClip(content(item))">
              <template #icon>
                <n-icon>
                  <ClipboardOutline/>
                </n-icon>
              </template>
            </n-button>
            <!--删除-->
            <n-button ghost size="small" disabled>
              <template #icon>
                <n-icon>
                  <TrashOutline/>
                </n-icon>
              </template>
            </n-button>
            <!--重试-->
            <n-button ghost size="small" v-show="item.role === 'user'" disabled>
              <template #icon>
                <n-icon>
                  <RefreshOutline/>
                </n-icon>
              </template>
            </n-button>
          </n-input-group>
        
        </div>
      
      </div>
    </n-infinite-scroll>
  </n-layout-content>
</template>

<script setup lang="ts">
import Text from "../../components/text/index.vue"
import Loding from "./components/layoutSider/loding.vue"
import {NButton, NIcon} from "naive-ui";
import {ClipboardOutline, Pencil, TrashOutline, RefreshOutline, ColorFill} from "@vicons/ionicons5";
import 'katex/dist/katex.min.css'
import '../../styles/lib/tailwind.css'
import '../../styles/lib/highlight.less'
import '../../styles/lib/github-markdown.less'
import {settings} from "../../stores/setting.ts";
import {copyToClip} from "../../utils/copy.ts";
import {inject} from "vue";

const isHeight = inject('innerHeight')
const config = settings().message_config;

/** 给组件指定初始值 */
const props = defineProps({
  messages: {
    type: Array,
    default: []
  },
  sendLoding: {
    type: Boolean,
    required: false,
  },
})

// 生成消息显示内容
const generateDisplay = (item: any) => {
  if (!item.id || !config.show_all) return ''; // 如果没有id或者总开关关闭，则不显示任何内容
  
  let output = '';
  
  // 显示模型名称（如果角色不是user并且开关开启）
  if (item.role !== 'user' && config.show_model) {
    output += '模型：' + item.model + ' | ';
  }
  
  if (item.usage && config.show_all) {
    if (typeof item.usage.prompt_tokens === 'number' && config.show_prompt_mark) {
      output += '提示令牌：' + item.usage.prompt_tokens + ' | ';
    }
    if (typeof item.usage.completion_tokens === 'number' && config.show_completion_token) {
      output += '完成令牌：' + item.usage.completion_tokens + ' | ';
    }
    if (typeof item.usage.total_tokens === 'number' && config.show_token_total) {
      output += '令牌总数：' + item.usage.total_tokens + ' | ';
    }
    if (item.usage.completion_tokens_details
      && typeof item.usage.completion_tokens_details.reasoning_tokens === 'number'
      && config.show_inference_token) {
      output += '推理令牌：' + item.usage.completion_tokens_details.reasoning_tokens + ' | ';
    }
  }
  
  return output ? output.slice(0, -3) : ''; // 移除最后一个多余的 " | "，如果output为空则返回空字符串
}

/*
* 内容
* */
const content = (value) => {
  if (value.role === 'user') {
    return value.content;
  } else if (value.status_code) {
    // todo 美化json
    return value.message;
  } else if (value.choices?.[0]?.delta?.content) {
    return value.choices[0].delta.content;
  }
  
  return ''; // 默认返回空字符串，避免 undefined 的情况
}

// 是否展示思考
const reasoning_content_show = (value) => {
  
  if (value.role == 'user') return false
  else return (!!value.choices?.[0]?.delta?.reasoning_content && config.think && config.show_all);
}

const reasoning_content = (value) => {
  return value.choices?.[0]?.delta?.reasoning_content ?? ""
}

</script>

<style scoped>
.message {
  
  &:hover .input-group {
    opacity: 1;
  }
  
  .input-group {
    opacity: 0;
  }
  
  &:last-child {
    margin-bottom: 0;
  }
  
}


</style>
