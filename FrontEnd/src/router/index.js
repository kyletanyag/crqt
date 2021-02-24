import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home'

import Callback from '@/views/Callback'
import ErrorPage from '@/views/Error'

//import { routeGuard } from '@/auth'

const routes = [

  {
      path: '/ContactUs',
      name: 'ContactUs',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ '../views/ContactUs.vue')
   },
  {
      path: '/SimulationResults',
      name: 'SimulationResults',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ '../views/SimulationResults.vue')
    },
    {
        path: '/TidyTree',
        name: 'TidyTree',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/TidyTree.vue')
    },
    {
        path: '/Robustness',
        name: 'Robustness',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/Robustness.vue')
    },
    {
        path: '/Resourcefullness',
        name: 'Resourcefullness',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/Resourcefullness.vue')
    },
    {
        path: '/ResilienceMetrics',
        name: 'ResilienceMetrics',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/ResilienceMetrics.vue')
    },
    {
        path: '/Redundancy',
        name: 'Redundancy',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/Redundancy.vue')
    },
    {
        path: '/Rapidity',
        name: 'Rapidity',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/Rapidity.vue')
    },
    {
        path: '/NetworkTopology',
        name: 'NetworkTopology',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/NetworkTopology.vue')
    },
    {
        path: '/ForceLayout',
        name: 'ForceLayout',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/ForceLayout.vue')
    },
    {
        path: '/ColorGraphView',
        name: 'ColorGraphView',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/ColorGraphView.vue')
    },
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/callback',
        name: 'Callback',
        component: Callback
    },
    {
        path: '/error',
        name: 'Error',
        component: ErrorPage,
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router