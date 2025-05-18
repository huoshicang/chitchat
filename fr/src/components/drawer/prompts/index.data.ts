
import instance from "../../../api/fach.ts";
import {ref} from "vue";
import type {originalType} from "./index";

// 新增框是否显示
export const showInner = ref<boolean>(false)
export const new_prompt = ref<originalType>({
  id: '',
  title: '',
  prompt: '',
})

// 输入框
export const searchValue = ref<string>('')

// 显示数据
export const data_list = ref<originalType[]>([])

// 关闭新增框
export const close = () => {
  new_prompt.value = {
    id: '',
    title: '',
    prompt: '',
  }
}

// 分享
export const share = async (id: string) => {
  const {status_code, _, message} = await instance.get(
    `prompts/share?prompts_id=${id}`,
  );

  if (status_code === 200) window.$message.success(message);
  else window.$message.warning(message);
};

// 删除
export const del = async (id: string) => {
  const {status_code, _, message} = await instance.get(
    `prompts/del?prompts_id=${id}`,
  );

  if (status_code === 200) window.$message.success(message);
  else window.$message.warning(message);
};

/**
 * 添加新模型
 * @param value 新模型的数据
 */
export const add = async (value) => {
  const {status_code, _, message} = await instance.post('prompts/new', value);

  if (status_code === 200) window.$message.success(message);
  else window.$message.warning(message);
};

/**
 * 编辑模型
 * @param value 编辑后的模型数据
 */
export const edit = async (value) => {
  const {status_code, _, message} = await instance.post('prompts/edit', value);

  if (status_code === 200) window.$message.success(message);
  else window.$message.warning(message);
};

/**
 * 表单验证规则
 */
export const rules = {
  title: {
    required: true,
    trigger: ['blur', 'input'],
    message: '请输入提示名称',
  },
  prompt: {
    required: true,
    trigger: ['blur', 'input'],
    message: '请输入提示内容',
  },
};
