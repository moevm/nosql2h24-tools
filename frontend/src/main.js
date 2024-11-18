import './assets/css/main.css'
import './js/axiosConfig.js'

import { createApp } from 'vue'
import App from './App.vue'
import router from './js/router.js'
import store from './js/store.js'

const app = createApp(App)

app.use(router)
app.use(store)

app.mount('#app')
