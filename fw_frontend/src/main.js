import './assets/main.css'
import { createApp } from 'vue'
// add in the pinia store
import { createPinia } from 'pinia'

import App from './App.vue'
// add in the vue router
import router from './router'
// get bootstrap styling
import 'bootstrap/dist/css/bootstrap.min.css'
const app = createApp(App)
// get bootstrap icons
import 'bootstrap-icons/font/bootstrap-icons.css'


app.use(createPinia())
app.use(router)

app.mount('#app')
