import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Mosaic from '../views/Mosaic.vue'
import AircraftDetail from '../views/AircraftDetail.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/about',
      name: 'About',
      component: About
    },
    {
      path: '/mosaic',
      name: 'Mosaic',
      component: Mosaic
    },
    {
      path: '/aircraft/:id',
      name: 'AircraftDetail',
      component: AircraftDetail,
      props: true
    }
  ]
})

export default router