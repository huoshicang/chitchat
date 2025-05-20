import { createWebHistory, createRouter } from 'vue-router'

import MianCenter from '../components/mianCenter.vue'; // 假设这是你的聊天室页面组件

const routes = [
  {
    path: '/',
    component: MianCenter
  },
  {
    path: '/chat/:id',
    component: MianCenter,
    props: true // 自动将 params 映射为组件的 props
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
