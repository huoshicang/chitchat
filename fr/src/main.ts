import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import NaiveUI from "naive-ui"
import { createPinia } from 'pinia'
import piniaPlug from "pinia-plugin-persistedstate";
import router from './router';


const pinia = createPinia()
pinia.use(piniaPlug)

const app = createApp(App)

app.use(pinia)
app.use(NaiveUI)
app.use(router)
app.mount('#app')


