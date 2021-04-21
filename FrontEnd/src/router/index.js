import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
      path: '/About',
      name: 'About',
      component: () => import(/* webpackChunkName: "ContactUs" */ '../views/About.vue')
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
        path: '/error/:errorCode',
        name: 'Error',
        component: () => import(/* webpackChunkName: "Error" */ '@/views/Error'),
        props: true,
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
        component: () => import(/* webpackChunkName: "Data Driven Results" */ '@/views/SimulationResults/DataDriven/Default.vue'),

    },
    {
        path: '/simulation-results/data-driven/summary',
        name: 'Data Driven Results - Summary',
        component: () => import(/* webpackChunkName: "Data Driven Results - Summary" */ '@/views/SimulationResults/DataDriven/Summary.vue')
    },
    {
        path: '/simulation-results/data-driven/overall-network-compromise',
        name: 'Data Driven Results - Overall Network Compromise',
        component: () => import(/* webpackChunkName: "Data Driven Results - Overall Network Compromise" */ '@/views/SimulationResults/DataDriven/OverallNetworkCompromise.vue')
    },
    {
        path: '/simulation-results/data-driven/derived-node-exploitation',
        name: 'Data Driven Results - Derived Node Exploitation',
        component: () => import(/* webpackChunkName: "Data Driven Results - Derived Node Exploitation" */ '@/views/SimulationResults/DataDriven/DerivedNodeExploitation.vue')
    },
    {
        path: '/simulation-results/data-driven/network-visualization',
        name: 'Data Driven Results - Network Visualization',
        component: () => import(/* webpackChunkName: "Data Driven Results - Network Visualization" */ '@/views/SimulationResults/DataDriven/NetworkVisualization.vue')
    },
    {
        path: '/simulation-results/data-driven/recommendations',
        name: 'Data Driven Results - Recommendations',
        component: () => import(/* webpackChunkName: "Data Driven Results - Recommendations" */ '@/views/SimulationResults/DataDriven/Recommendations.vue')
    },
    {
        path: '/simulation-results/data-driven/printout',
        name: 'Data Driven Results - Printout',
        component: () => import(/* webpackChunkName: "Data Driven Results - Printout" */ '@/views/SimulationResults/DataDriven/Printout.vue')
    },
    {
        path: '/simulation-results/model-driven/',
        name: 'Model Driven Results',
        component: () => import(/* webpackChunkName: "Model Driven Result" */ '@/views/SimulationResults/ModelDriven/Default.vue')
    },
    {
        path: '/simulation-results/model-driven/summary',
        name: 'Model Driven Results - Summary',
        component: () => import(/* webpackChunkName: "Model Driven Results - Summary" */ '@/views/SimulationResults/ModelDriven/Summary.vue')
    },
    {
        path: '/simulation-results/model-driven/network-visualization',
        name: 'Model Driven Results - Network Visualization',
        component: () => import(/* webpackChunkName: "Model Driven Results - Network Visualization" */ '@/views/SimulationResults/ModelDriven/NetworkVisualization.vue')
    },
    {
        path: '/simulation-results/model-driven/graph-metrics',
        name: 'Model Driven Results - Graph Metrics',
        component: () => import(/* webpackChunkName: "Model Driven Results - Graph Metrics" */ '@/views/SimulationResults/ModelDriven/GraphMetrics.vue')
    },
    {
        path: '/simulation-results/model-driven/attack-path-metrics',
        name: 'Model Driven Results - Attack Path Metrics',
        component: () => import(/* webpackChunkName: "Model Driven Results - Node Specific Metrics" */ '@/views/SimulationResults/ModelDriven/AttackPathMetrics.vue')
    },
    {
        path: '/simulation-results/model-driven/severity-display',
        name: 'Model Driven Results - Severity Display',
        component: () => import(/* webpackChunkName: "Model Driven Results - Severity Display" */ '@/views/SimulationResults/ModelDriven/SeverityDisplay.vue')
    },
    {
        path: '/simulation-results/model-driven/recommendations',
        name: 'Model Driven Results - Recommendations',
        component: () => import(/* webpackChunkName: "Model Driven Results - Recommendations" */ '@/views/SimulationResults/ModelDriven/Recommendations.vue')
    },
    {
        path: '/simulation-results/model-driven/printout',
        name: 'Model Driven Results - Printout',
        component: () => import(/* webpackChunkName: "Model Driven Results - Printout" */ '@/views/SimulationResults/ModelDriven/Printout.vue')
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router