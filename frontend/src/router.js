import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './views/HomeView.vue';
import CategoryView from './views/CategoryView.vue';
import ShoppingCartView from './views/ShoppingCartView.vue';
import CheckoutView from './views/CheckoutView.vue';
import ProfileView from './views/ProfileView.vue';
import LoginView from './components/LoginView.vue';
import RegisterView from './components/RegisterView.vue';
import ImageDetailView from './views/ImageDetailView.vue';
import OrderSuccessView from './views/OrderSuccessView.vue';
import ChangeNameView from './views/ChangeNameView.vue';
import ChangeEmailView from './views/ChangeEmailView.vue';
import ChangePasswordView from './views/ChangePasswordView.vue';
import ChangeAddressView from './views/ChangeAddressView.vue';
import ViewOrdersView from './views/ViewOrdersView.vue';
import SearchResultsView from './components/SearchResultsView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/category/:categoryName', component: CategoryView },
    { path: '/photos/:id', component: ImageDetailView },
    { path: '/shopping-cart', component: ShoppingCartView },
    { path: '/checkout', component: CheckoutView },
    { path: '/profile', component: ProfileView },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/order-success/:orderId', name: 'OrderSuccessView', component: OrderSuccessView },
    { path: '/change-name', component: ChangeNameView },
    { path: '/change-email', component: ChangeEmailView },
    { path: '/change-password', component: ChangePasswordView },
    { path: '/change-address', component: ChangeAddressView },
    { path: '/view-orders', component: ViewOrdersView },
    { path: '/search-results/:query', name: 'search-results', component: SearchResultsView, props: route => ({ searchQuery: route.params.query })},
  ],
});

export default router;
