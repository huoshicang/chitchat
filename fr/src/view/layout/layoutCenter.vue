<template>
  <n-layout-content position="absolute" style="top: 64px; bottom: 140px" content-style="padding: 24px;"
                    :native-scrollbar="false">
    <n-infinite-scroll :distance="10">
      <div
        v-for="(item, index) in props.messages"
        :key="index"
        class="message flex mb-2.5"
        :class="item.role === 'user' ? 'flex-row-reverse ml-12.5 mr-0' : 'ml-0 mr-12.5'"
      >
        
        <img class="w-7 h-7 rounded-full" :class="item.role === 'user' ? 'ml-2' : 'mr-2'"
             src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg" alt="">
        <div class="flex flex-col" :class="item.role === 'user' ? 'items-end' : 'items-start'">
          
          <n-collapse arrow-placement="right"
                      class="ml-3"
                      v-if="item.role != 'user' &&
                      item.choices[0].delta.reasoning_content &&
                      config.think"
                      :default-expanded-names="[expandedName]">
            <n-collapse-item title="思考" :name="item.created" v-if="config.showAll">
              <Text :text="item.choices[0].delta.reasoning_content "/>
            </n-collapse-item>
          </n-collapse>
          
          <Text :text="item.role === 'user' ? item.content : item.choices[0].delta.content"/>
          <div v-if="item.role !== 'user' && config.showAll">
            <n-text depth="3" class="ml-3"> {{ generateDisplay(item) }}
              <span  v-if="config.showTime && item.created">
                 | <n-time :time="item.created" unix/>
              </span>
            </n-text>
          </div>
          <n-input-group class="input-group">
            <n-button ghost size="small">
              <template #icon>
                <n-icon>
                  <ChatbubblesOutline/>
                </n-icon>
              </template>
            </n-button>
            <n-button ghost size="small">
              <template #icon>
                <n-icon>
                  <TrashOutline/>
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
import {NButton, NIcon} from "naive-ui";
import {ChatbubblesOutline, TrashOutline} from "@vicons/ionicons5";
import {onMounted, ref, watch} from "vue";
import 'katex/dist/katex.min.css'
import '../../styles/lib/tailwind.css'
import '../../styles/lib/highlight.less'
import '../../styles/lib/github-markdown.less'
import {settings} from "../../stores/setting.ts";

const config = settings().messageConfig;

/** 给组件指定初始值 */
const props = defineProps({
  messages: {
    type: Array,
    default: []
  },
})

// 展开
const expandedName = ref<string>("")

// 生成消息显示内容
const generateDisplay = (item: any) => {
  if (!item.id || !config.showAll) return ''; // 如果没有id或者总开关关闭，则不显示任何内容
  
  let output = '';
  
  // 显示模型名称（如果角色不是user并且开关开启）
  if (item.role !== 'user' && config.showModel) {
    output += '模型：' + item.model + ' | ';
  }
  
  if (item.usage && config.showAll) {
    if (typeof item.usage.prompt_tokens === 'number' && config.showPromptTokens) {
      output += '提示令牌：' + item.usage.prompt_tokens + ' | ';
    }
    if (typeof item.usage.completion_tokens === 'number' && config.showCompletionTokens) {
      output += '完成令牌：' + item.usage.completion_tokens + ' | ';
    }
    if (typeof item.usage.total_tokens === 'number' && config.showTotalTokens) {
      output += '令牌总数：' + item.usage.total_tokens + ' | ';
    }
    if (item.usage.completion_tokens_details
      && typeof item.usage.completion_tokens_details.reasoning_tokens === 'number'
      && config.showReasoningTokens) {
      output += '推理令牌：' + item.usage.completion_tokens_details.reasoning_tokens + ' | ';
    }
  }
  
  return output ? output.slice(0, -3) : ''; // 移除最后一个多余的 " | "，如果output为空则返回空字符串
}

onMounted(() => {

})

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
