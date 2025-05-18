<template>
  <n-input-group>
    <n-input v-model:value="searchValue" type="text" placeholder=""/>
    <n-button type="primary" ghost @click="showInner = true">
      新增
    </n-button>
  </n-input-group>
  <n-drawer v-model:show="showInner" :width="450" @after-leave="close">
    <n-drawer-content title="新增提示">
      <New :new_prompt="new_prompt"/>
    </n-drawer-content>
  </n-drawer>
  
  <n-divider title-placement="left">
    我的
  </n-divider>
  <n-flex>
    <n-popover trigger="hover" v-for="(item, index) in data_list.my" :key="item._id">
      <template #trigger>
        <n-card size="small" class="n-card">
          <template #header>
            <n-ellipsis style="max-width: 140px" :tooltip="false">
              {{ item.title }}
            </n-ellipsis>
          </template>
          <template #header-extra>
            <n-dropdown trigger="hover" :options="options('my', item)" @select="handleSelect">
              <n-button text class="n-card-header-extra">
                <n-icon>
                  <EllipsisVerticalOutline/>
                </n-icon>
              </n-button>
            </n-dropdown>
          </template>
        </n-card>
      </template>
      <template #header>
        {{ item.prompt }}
      </template>
      {{ item.title }}
    </n-popover>
  </n-flex>
  
  <n-divider title-placement="left">
    公共
  </n-divider>
  
  <n-flex>
    <n-popover trigger="hover" v-for="(item, index) in data_list.public" :key="item._id">
      <template #trigger>
        <n-card size="small" class="n-card">
          <template #header>
            <n-ellipsis style="max-width: 140px" :tooltip="false">
              {{ item.title }}
            </n-ellipsis>
          </template>
          <template #header-extra>
            <n-dropdown trigger="hover" :options="options('', item)" @select="handleSelect">
              <n-button text class="n-card-header-extra">
                <n-icon>
                  <EllipsisVerticalOutline/>
                </n-icon>
              </n-button>
            </n-dropdown>
          </template>
        </n-card>
      </template>
      <template #header>
        {{ item.prompt }}
      </template>
      {{ item.title }}
    </n-popover>
  </n-flex>
  
  <n-divider title-placement="left">
    分享
  </n-divider>
  <n-flex>
    <n-popover trigger="hover" v-for="(item, index) in data_list.others" :key="item._id">
      <template #trigger>
        <n-card size="small" class="n-card">
          <template #header>
            <n-ellipsis style="max-width: 140px" :tooltip="false">
              {{ item.title }}
            </n-ellipsis>
          </template>
          <template #header-extra>
            <n-dropdown trigger="hover" :options="options('', item)" @select="handleSelect">
              <n-button text class="n-card-header-extra">
                <n-icon>
                  <EllipsisVerticalOutline/>
                </n-icon>
              </n-button>
            </n-dropdown>
          </template>
        </n-card>
      </template>
      <template #header>
        {{ item.prompt }}
      </template>
      {{ item.title }}
    </n-popover>
  </n-flex>
  
  <!--<n-list hoverable clickable>-->
  <!--  <n-list-item v-for="(item, index) in data_list" :key="item._id">-->
  <!--    <template #suffix>-->
  <!--      <n-space>-->
  <!--        <n-button-group>-->
  <!--          <n-button @click="">-->
  <!--            删除-->
  <!--          </n-button>-->
  <!--          <n-button @click="new_prompt = item">-->
  <!--            修改-->
  <!--          </n-button>-->
  <!--        </n-button-group>-->
  <!--        <n-button-group>-->
  <!--          <n-button>-->
  <!--            使用-->
  <!--          </n-button>-->
  <!--          <n-button @click="share(item._id)" v-show="item._id == user_id">-->
  <!--            分享-->
  <!--          </n-button>-->
  <!--        </n-button-group>-->
  <!--      </n-space>-->
  <!--    -->
  <!--    </template>-->
  <!--    <n-thing>-->
  <!--      <template #header>-->
  <!--      </template>-->
  <!--      {{ item.prompt }}-->
  <!--    </n-thing>-->
  <!--  </n-list-item>-->
  <!--</n-list>-->
</template>

<script setup lang="ts">
import {h, onMounted, ref, watch} from "vue";
import {EllipsisVerticalOutline} from '@vicons/ionicons5'
import instance from "../../../api/fach.ts";
import {NText, useMessage} from "naive-ui";
import type {DropdownOption} from 'naive-ui'
import New from "./new.vue"
import {share, del, close, showInner, new_prompt, data_list, searchValue} from "./index.data.ts";
import {settings} from "../../../stores/setting.ts";
import {info} from "../../../stores/info.ts";
import {useRouter} from "vue-router";

const router = useRouter();
const config = settings().promptsConfig;
const set_prompt = info().set_prompt
const msg = useMessage()
// 原始数据
let original = {}


const options = (flag: string = "", value: any) => {
  const baseOptions: DropdownOption[] = [
    {label: '使用', key: 'use', ...value}
  ];
  
  if (flag === "my") {
    baseOptions.push(
      {label: '删除', key: 'del', ...value},
      {label: '修改', key: 'edit', ...value},
      {
        label: config.share
          ? () => h(NText, {type: value.share ? 'success' : 'error'}, {default: () => '分享'})
          : '分享',
        key: 'share',
        ...value
      }
    );
  }
  
  return baseOptions;
};


const handleSelect = (key: string | number, option: DropdownOption) => {
  if (key === 'del') del(option._id)
  else if (key === 'edit') new_prompt.value = option
  else if (key === 'share') share(option._id)
  else if (key === 'use') {
    router.push(`/`)
    set_prompt(option.prompt)
  }
}

// 获取数据
const getData = async () => {
  const {status_code, data, message} = await instance.get(`prompts/porompts`);
  if (status_code === 200) {
    original = data
    console.log(original)
    data_list.value = data
  } else msg.warning(message);
}


onMounted(async () => {
  await getData()
})

watch(
  [() => searchValue.value, () => new_prompt.value],
  ([newValue, newPrompt]) => {
    
    // 搜索
    if (newValue == ""){
      console.log('newValue', newValue)
      console.log('original', original)
      console.log('data_list.value', data_list.value)
      data_list.value = original
    }
    else {
      data_list.value.my = original.my.filter((item) => item.title.includes(newValue));
      data_list.value.others = original.others.filter((item) => item.title.includes(newValue));
      data_list.value.public = original.public.filter((item) => item.title.includes(newValue));
      
      console.log(original)
      
    }
    
    // 新增
    if (newPrompt.title) showInner.value = true
    
  },
  {
    immediate: true
  }
)

</script>

<style lang="less" scoped>

.n-card {
  width: 200px;
  
  &:hover {
    .n-card-header-extra {
      display: block;
    }
  }
  
  .n-card-header-extra {
    display: none;
    font-size: 16px;
  }
}


</style>
