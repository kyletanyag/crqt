import { createApp } from 'vue'
import VueNumberInput from '@chenfengyuan/vue-number-input';
import App from './App.vue'
import router from './router'
import store from './store'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

// Front-End Branch Test

// Import the Auth0 configuration
import authConfig from "../auth-config.json";

// Import the plugin here
import { setupAuth } from "./auth";

const app = createApp(App)
    .use(store)
    .use(router)
    .component(VueNumberInput.name, VueNumberInput);

function callbackRedirect(appState) {
    router.push(
        appState && appState.targetUrl
            ? appState.targetUrl
            : '/'
    );
}

setupAuth(authConfig, callbackRedirect).then((auth) => {
    app.use(auth).mount('#app')
})
