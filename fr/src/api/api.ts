import{ my_post, my_get } from "./MyAxios";
import type {del_model, prompts} from "./data";
import type {originalType} from "../components/drawer/prompts";


export const Api = {
  // 获取验证信息
  auth: async (): Promise<any> => {
    return await my_get("auth", {});
  },

  // 获取提示
  get_prompts: async (): Promise<any> => {
    return await my_get("prompts/porompts", {});
  },

  // 分享提示
  share_prompts: async (data: prompts): Promise<any> => {
    return await my_get("prompts/share", data);
  },

  // 删除提示
  del_prompts: async (value: prompts): Promise<any> => {
    return await my_get(`prompts/del`, value);
  },

  // 新增提示
  new_prompts: async (value: originalType): Promise<any> => {
    return await my_post(`prompts/new`, value);
  },

  // 修改提示
  edit_prompts: async (value: originalType): Promise<any> => {
    return await my_post(`prompts/edit`, value);
  },

  get_chat: async (): Promise<any> => {
    return await my_get('chats/chat', {});
  },

  get_message: async (value: string): Promise<any> => {
    return await my_get(`messages/${value}`, {});
  },

  get_model: async (): Promise<any> => {
    return await my_get('model/model', {});
  },

  del_model: async (value: del_model): Promise<any> => {
    return await my_get(`model/del`, value);
  },

  new_model: async (value): Promise<any> => {
    return await my_post(`model/new`, value);
  },

  edit_model: async (value): Promise<any> => {
    return await my_post(`model/new`, value);
  },

};
