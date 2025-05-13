import type { SelectBaseOption } from 'naive-ui';
import { model } from '../../../stores/model.ts';
import instance from '../../../api/fach.ts';

/**
 * 设置模型的默认值
 * @param id 模型ID
 */
const setModel = (id: string | null = null) => {
  const Model = model();

  Model.setModel(
    id,
    '',
    {
      model: '',
      temperature: null,
      top_p: null,
    },
    {
      api_key: '',
      base_url: '',
    },
    [],
  );
};

/**
 * 模型选择框事件处理函数
 * @param value 选中的值
 * @param option 选中项
 */
export const change = (
  value: Array<string> | string | number | null,
  option: SelectBaseOption | null | SelectBaseOption[],
) => {
  const setModelValue = model();

  setModelValue.setModel(
    option._id,
    option.name,
    option.model_var,
    option.ai_var,
    option.extra,
  );
};

/**
 * 复制当前模型设置
 */
export const copy = () => {
  const Model = model();
  const ModelValue = model().modelValue;

  Model.setModel(
    '',
    `${ModelValue.name}（复制）`,
    ModelValue.model_var,
    ModelValue.ai_var,
    ModelValue.extra,
  );
};

/**
 * 删除模型
 */
export const del = async () => {
  const Model = model();

  const { status_code, _, message } = await instance.get(
    `model/del?model_id=${Model.modelValue.id}`,
  );

  if (status_code === 200) {
    window.$message.success(message);
    setModel();
  } else {
    window.$message.warning(message);
  }
};

/**
 * 添加新模型
 * @param value 新模型的数据
 */
export const add = async (value) => {
  const { status_code, _, message } = await instance.post('model/new', value);

  if (status_code === 200) {
    window.$message.success(message);
    setModel();
  } else {
    window.$message.warning(message);
  }
};

/**
 * 编辑模型
 * @param value 编辑后的模型数据
 */
export const edit = async (value) => {
  const { status_code, _, message } = await instance.post('model/edit', value);

  if (status_code === 200) {
    window.$message.success(message);
    setModel();
  } else {
    window.$message.warning(message);
  }
};

/**
 * 表单验证规则
 */
export const rules = {
  name: {
    required: true,
    trigger: ['blur', 'input'],
    message: '请输入模型名称',
  },
  ai_var: {
    api_key: {
      required: true,
      trigger: ['blur', 'input'],
      message: '请输入key',
    },
    base_url: {
      required: true,
      trigger: ['blur', 'input'],
      message: '请输入端点',
    },
  },
  model_var: {
    model: {
      required: true,
      trigger: ['blur', 'input'],
      message: '请输入模型名称',
    },
    temperature: {
      required: true,
      trigger: ['blur', 'input'],
      message: '请输入采样温度',
    },
    top_p: {
      required: true,
      trigger: ['blur', 'input'],
      message: '请输入采样率',
    },
  },
};
