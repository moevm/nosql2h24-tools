import './assets/css/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './js/router.js'

const app = createApp(App)

app.use(router)

app.mount('#app')
