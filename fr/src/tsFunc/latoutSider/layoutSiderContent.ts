import type {Component} from "vue";
import {h} from "vue";
import {NIcon} from "naive-ui";
import {ChatboxEllipsesOutline} from '@vicons/ionicons5'
import {type MenuOption, NDropdown, NEllipsis} from "naive-ui";
// 菜单操作
interface OPTIONSItem {
  label: string;
  key: string;
}
// 菜单操作
interface MenuOptionItem {
  label: string;
}

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

const handleSelect = (key: string | number): void => {
  console.log(key)
}


export const renderIcon = (icon: Component): vNode => {
  return () => h(NIcon, null, {default: () => h(icon)})
}

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
