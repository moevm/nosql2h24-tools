import { createApp } from 'vue'
import VueAwesomePaginate from "vue-awesome-paginate"
import Toast, {POSITION} from "vue-toastification"

import App from './App.vue'
import router from './js/router.js'
import store from './js/store.js'

import './assets/css/main.css'
import './js/axiosConfig.js'
import "vue-awesome-paginate/dist/style.css";

import "vue-toastification/dist/index.css";

const app = createApp(App)

store.dispatch('checkLocalStorage');

app.use(router)
app.use(store)
app.use(VueAwesomePaginate)
app.use(Toast, {
  position: POSITION.TOP_CENTER,
})

app.mount('#app')
