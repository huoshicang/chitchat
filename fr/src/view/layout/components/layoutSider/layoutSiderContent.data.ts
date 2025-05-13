import type {Component} from "vue";
import {h} from "vue";
import {NDropdown, NEllipsis, NIcon, NText} from "naive-ui";
import {type MenuOption, type DropdownOption} from "naive-ui";
import type {OPTIONSItem, MenuOptionItem} from "./layoutSiderContent";
import {settings} from "../../../../stores/setting.ts";
import instance from "../../../../api/fach.ts";


// 菜单操作
const options = (item: MenuActionItem): OPTIONSItem[] => {
  const config = settings().siderContent;


  const baseOptions: OPTIONSItem[] = [
    //{ label: '修改', key: 'modification' },
    {label: '删除', key: 'delete'}
  ];

// 添加分享选项
  baseOptions.push({
    label: config.display && config.share
      ? () => h(NText, {type: item.share ? 'success' : 'error'}, {default: () => '分享'})
      : '分享',
    key: 'share'
  });

  // 添加归档选项
  baseOptions.push({
    label: config.display && config.archive
      ? () => h(NText, {type: item.archive ? 'success' : 'error'}, {default: () => '归档'})
      : '归档',
    key: 'archive'
  });

  // 添加ID显示（如果配置允许）
  if (config.display && config.id) {
    baseOptions.unshift({
      key: 'header',
      type: 'render',
      render: () => h(
        'div',
        {style: 'display: flex; align-items: center; padding: 8px 12px;'},
        [h(NText, {depth: 3}, {default: () => `id：${item._id}`})]
      )
    });
  }

  return baseOptions.map(i => {
    return {
      ...i,
      id: item._id
    };
  });
};


/**
 * 菜单下拉事件
 *
 * @param key 菜单的key
 * @param option 选项对象
 * @returns void
 */
const handleSelect = async (key: string | number, option: DropdownOption): void => {

  const urlMap = {
    archive: `chats/archive?chat_id=${option.id}`,
    delete: `chats/del?chat_id=${option.id}`,
    share: `chats/share?chat_id=${option.id}`
  };

  switch (key) {
    case 'modification':
      console.log('修改');
      break;
    case 'archive':
    case 'delete':
    case 'share':
      const url = urlMap[key as keyof typeof urlMap];

      const {status_code, _, message} = await instance.get(url)
      if (status_code === 200) window.$message.success(message)
      else window.$message.warning(message)

      break;
    default:
      break;
  }


}

/**
 * 渲染图标组件的函数
 *
 * @param icon 图标组件
 * @returns vNode
 */
export const renderIcon = (icon: Component): vNode => {
  return () => h(NIcon, null, {default: () => h(icon)})
}

/**
 * 生成并返回一组格式化后的菜单选项
 *
 * @param menuOptions 菜单选项的数组，每个选项包含菜单的标签和其他信息默认为空数组
 * @returns 返回格式化后的菜单选项数组
 */
export const setMenuOptions = (menuOptions: MenuOptionItem[] = []): MenuOption => {

  return menuOptions.map((item, _): MenuOption => {
    return {
      label: () => {
        return h(NEllipsis, {}, h(NDropdown, {
            placement: 'bottom-start',
            trigger: 'hover',
            size: 'small',
            options: options(item),
            onSelect: handleSelect
          },
          {
            default: item.title
          }))
      },
      key: item.message_id,
      title: item.title
      //icon: renderIcon(ChatboxEllipsesOutline)
    }
  })
}
