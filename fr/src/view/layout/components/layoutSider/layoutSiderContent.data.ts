import type {Component} from "vue";
import {h} from "vue";
import {NIcon} from "naive-ui";
import {ChatboxEllipsesOutline} from '@vicons/ionicons5'
import {type MenuOption, NDropdown, NEllipsis} from "naive-ui";
import type {OPTIONSItem, MenuOptionItem} from "./layoutSiderContent";


// 菜单操作
const OPTIONS: OPTIONSItem[] = [
  {
    label: '修改',
    key: 'modification'
  },
  {
    label: '归档',
    key: 'archiving'
  },
  {
    label: '删除',
    key: 'delete'
  },
  {
    label: '分享',
    key: 'share'
  }
]

/**
 * 菜单下拉事件
 *
 * @param key 菜单的key
 * @returns void
 */
const handleSelect = (key: string | number): void => {
  console.log(key)
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

  return menuOptions.map((item, index): MenuOption => {
    return {
      label: () => {
        return h('div', {}, [
          h(NEllipsis, {}, h(NDropdown, {
              placement: 'bottom-start',
              trigger: 'hover',
              size: 'small',
              options: OPTIONS,
              onSelect: handleSelect
            },
            {
              default: item.label
            })),
        ])
      },
      key: index,
      icon: renderIcon(ChatboxEllipsesOutline)
    }
  })
}
