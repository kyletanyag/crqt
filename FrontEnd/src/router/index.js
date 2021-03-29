import { createRouter, createWebHistory } from 'vue-router'

// Do we need these?
import Callback from '@/views/Callback'
import ErrorPage from '@/views/Error'
import SecureComponent from "@/views/Secure.vue"

// Testing page for Kyle
import Sandbox from "../views/_Sandbox.vue";

const routes = [
    {
      path: '/ContactUs',
      name: 'ContactUs',
      component: () => import(/* webpackChunkName: "ContactUs" */ '../views/ContactUs.vue')
    },
    {
      path: '/SimulationResults',
      name: 'SimulationResults',
      component: () => import(/* webpackChunkName: "SimulationResults" */ '../views/SimulationResults/SimulationResults.vue')
    },
    {
        path: '/network-topology/data-driven',
        name: 'Data Driven',
        component: () => import(/* webpackChunkName: "Data-Driven-Input" */ '../views/NetworkTopology/DataDriven.vue')
    },
    {
        path: '/network-topology/model-driven',
        name: 'Model Driven',
        component: () => import(/* webpackChunkName: "Model-Driven-Input" */ '../views/NetworkTopology/ModelDriven.vue')
    },
    {
        path: '/',
        name: 'Home',
        component: () => import(/* webpackChunkName: "Home" */ '@/views/Home.vue'),
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
        component: () => import(/* webpackChunkName: "Login" */ '@/views/Login/Login.vue'),
    },
    {
        path: '/login/qr/:id',
        name: 'QR Login',
        component: () => import(/* webpackChunkName: "QR Login" */ '@/views/Login/QRLogin.vue'),
        props: true,
    },
    {
        path: '/register',
        name: "Register",
        component: () => import(/* webpackChunkName: "Registration" */ '@/views/Login/Register.vue'),
    },
    {
        path: '/sandbox',
        name: 'Sandbox',
        component: Sandbox
    },
    {
        path: '/qr/:id',
        name: 'QR Setup',
        component: () => import(/* webpackChunkName: "QR Setup" */ '@/views/Login/QRCode.vue'),
        props: true
    },
    {
        path: '/admin',
        name: 'Admin',
        component: () => import(/* webpackChunkName: "Admin" */ '@/views/Admin/Admin.vue'),
        props: true
    },
    {
        path: '/simulation-results/data-driven',
        name: 'Data Driven Results',
        component: () => import(/* webpackChunkName: "Data Driven Results" */ '@/views/SimulationResults/DataDrivenResults.vue')
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router