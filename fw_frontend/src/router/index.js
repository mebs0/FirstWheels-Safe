

import { createRouter, createWebHistory } from 'vue-router'

// all the pages of the apps frontend, need to import then so routes can be linked with them
import enterreg from '../subpages/enterreg.vue'
import inforesult from '../subpages/inforesult.vue'
import carchecklist from '../subpages/carchecklist.vue'
import settings from '../subpages/settings.vue'
import login from '../subpages/login.vue'
import usergarage from '../subpages/usergarage.vue'

// making the paths that link up to the pages
const routes = [
  { path: '/', component: enterreg },
  { path: '/result', component: inforesult },
  { path: '/checklist', component: carchecklist },
  { path: '/settings', component: settings },
  { path: '/login', component: login },
  { path: '/garage', component: usergarage },
]
// create the router using the routes defined and enable history mode for easy go back buttons and then export 
const menurouter = createRouter({history: createWebHistory(),routes,})
export default menurouter
