<!-- Navbar.vue -->
<template>
  <nav class="bg-gray-800 p-4">
    <div class="container mx-auto flex justify-between items-center">
      <div class="flex items-center space-x-4">
        <router-link to="/category/Cities" class="hover:text-gray-300 px-4 py-2 rounded-md bg-gray-600 hover:bg-gray-700">Cities</router-link>
        <router-link to="/category/Landscapes" class="hover:text-gray-300 px-4 py-2 rounded-md bg-gray-600 hover:bg-gray-700">Landscapes</router-link>
        <router-link to="/category/Street Photography" class="hover:text-gray-300 px-4 py-2 rounded-md bg-gray-600 hover:bg-gray-700">Street Photography</router-link>
      </div>
      <router-link to="/" class="text-lg font-bold flex-grow text-center text-white">SnapStock Licensing & Prints</router-link>
      <div class="flex space-x-4">
        <router-link v-if="!isAuthenticated" to="/login" class="hover:text-gray-300 px-4 py-2 rounded-md bg-blue-500 hover:bg-blue-700">Login</router-link>
        <router-link v-if="!isAuthenticated" to="/register" class="hover:text-gray-300 px-4 py-2 rounded-md bg-green-500 hover:bg-green-700">Sign Up</router-link>
        <router-link v-if="isAuthenticated" to="/shopping-cart" class="hover:text-gray-300 px-4 py-2 rounded-md bg-gray-500 hover:bg-gray-600">
          <font-awesome-icon :icon="['fas', 'shopping-cart']" />
        </router-link>
        <router-link v-if="isAuthenticated" to="/profile" class="hover:text-gray-300 px-4 py-2 rounded-md bg-green-500 hover:bg-green-700">
          <font-awesome-icon :icon="['fas', 'user-circle']" />
        </router-link>
        <a v-if="isAuthenticated" @click="logout" class="logout-link hover:text-gray-300 px-4 py-2 rounded-md bg-red-500 hover:bg-red-700">Logout</a>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

export default {
  components: {
    FontAwesomeIcon,
  },
  computed: {
    isAuthenticated() {
      // Access the authentication state from Vuex
      return !!this.$store.state.authToken;
    },
  },
  methods: {
    logout() {
      axios.post('http://127.0.0.1:5000/logout', null, {
        headers: {
          Authorization: `Bearer ${this.$store.state.authToken}`,
        },
      })
        .then(() => {
          // Clear the authentication token in Vuex
          this.$store.dispatch('logout');
          this.$router.push('/');
        })
        .catch(error => {
          console.error('Logout failed:', error);
        });
    },
  },
};
</script>

<style scoped>
.logout-link {
  cursor: pointer;
}
</style>

