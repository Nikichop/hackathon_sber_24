import { createMemoryHistory, createRouter } from 'vue-router'

import MainPage from '../components/MainPage.vue';

const routes = [
  { path: '/', component: MainPage },
]

export default createRouter({
  history: createMemoryHistory(),
  routes,
})
