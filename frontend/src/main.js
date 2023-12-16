// main.js
import { createApp } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faShoppingCart, faUserCircle } from '@fortawesome/free-solid-svg-icons';
import App from './App.vue';
import router from './router';
import store from './store/store'; 
import './assets/css/tailwind.css';

// Configure FontAwesome
library.add(faShoppingCart, faUserCircle);

const app = createApp(App);

// Register the FontAwesome component globally
app.component('font-awesome-icon', FontAwesomeIcon);

app.use(router);
app.use(store);

app.mount('#app');
