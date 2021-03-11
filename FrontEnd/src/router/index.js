import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home'

import Callback from '@/views/Callback'
import ErrorPage from '@/views/Error'

import LoginComponent from "../views/Login.vue"
import Login from "../views/Login.vue"
import SecureComponent from "../views/Secure.vue"
import QRLogin from '../views/QRLogin.vue'

import Sandbox from "../views/_Sandbox.vue";
import Register from "../views/Register.vue"

//import { routeGuard } from '@/auth'

const routes = [

  {
      path: '/ContactUs',
      name: 'ContactUs',
      component: () => import(/* webpackChunkName: "ContactUs" */ '../views/ContactUs.vue')
   },
  {
      path: '/SimulationResults',
      name: 'SimulationResults',
      component: () => import(/* webpackChunkName: "SimulationResults" */ '../views/SimulationResults.vue')
    },
    {
        path: '/TidyTree',
        name: 'TidyTree',
        component: () => import(/* webpackChunkName: "about" */ '../views/TidyTree.vue')
    },
    {
        path: '/Robustness',
        name: 'Robustness',
        component: () => import(/* webpackChunkName: "about" */ '../views/Robustness.vue')
    },
    {
        path: '/Resourcefullness',
        name: 'Resourcefullness',
        component: () => import(/* webpackChunkName: "about" */ '../views/Resourcefullness.vue')
    },
    {
        path: '/ResilienceMetrics',
        name: 'ResilienceMetrics',
        component: () => import(/* webpackChunkName: "about" */ '../views/ResilienceMetrics.vue')
    },
    {
        path: '/Redundancy',
        name: 'Redundancy',
        component: () => import(/* webpackChunkName: "about" */ '../views/Redundancy.vue')
    },
    {
        path: '/Rapidity',
        name: 'Rapidity',
        component: () => import(/* webpackChunkName: "about" */ '../views/Rapidity.vue')
    },
    {
        path: '/network-topology/data-driven',
        name: 'Data Driven',
        component: () => import(/* webpackChunkName: "Data-Driven-Input" */ '../views/DataDriven.vue')
    },
    {
        path: '/network-topology/model-driven',
        name: 'Model Driven',
        component: () => import(/* webpackChunkName: "Model-Driven-Input" */ '../views/ModelDriven.vue')
    },
    {
        path: '/ForceLayout',
        name: 'ForceLayout',
        component: () => import(/* webpackChunkName: "about" */ '../views/ForceLayout.vue')
    },
    {
        path: '/hello',
        name: 'hello',
        component: () => import(/* webpackChunkName: "about" */ '../views/ForceLayout.vue')
    },
    {
        path: '/ColorGraphView',
        name: 'ColorGraphView',
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
    },
    {
        path: '/secure',
        name: "Secure",
        component: SecureComponent
    },
    {
        path: '/login',
        name: "Login",
        component: Login, LoginComponent
    },
    {
        path: '/login/qr/:id',
        name: 'QR Login',
        component: QRLogin,
        props: true,
    },
    {
        path: '/register',
        name: "Register",
        component: Register
    },
    {
        path: '/sandbox',
        name: 'Sandbox',
        component: Sandbox
    },
    {
        path: '/qr/:id',
        name: 'QR Setup',
        component: () => import(/* webpackChunkName: "QR Setup" */ '../views/QRCode.vue'),
        props: true
    },
    {
        path: '/admin',
        name: 'Admin',
        component: () => import(/* webpackChunkName: "Admin" */ '../views/Admin.vue'),
        props: true
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router