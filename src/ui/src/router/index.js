import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Mosaic from '../views/Mosaic.vue'
import AircraftDetail from '../views/AircraftDetail.vue'
import Manufacturers from '../views/Manufacturers.vue'
import ManufacturerDetail from '../views/ManufacturerDetail.vue'

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
    },
    {
      path: '/manufacturers',
      name: 'Manufacturers',
      component: Manufacturers
    },
    {
      path: '/manufacturers/:id',
      name: 'ManufacturerDetail',
      component: ManufacturerDetail,
      props: true
    }
  ]
})

export default router