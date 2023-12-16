<template>
  <div class="bg-gray-900 text-white min-h-screen py-6 sm:py-8 lg:py-12">
    <form @submit.prevent="login" class="max-w-md mx-auto mt-8">
      <div class="mb-4">
        <label for="email" class="text-white block mb-2">Email:</label>
        <input v-model="email" id="email" name="email" type="email" class="rounded-md px-4 py-2 w-full bg-gray-900 text-white">
      </div>
      
      <div class="mb-4">
        <label for="password" class="text-white block mb-2">Password:</label>
        <input v-model="password" id="password" name="password" type="password" class="rounded-md px-4 py-2 w-full bg-gray-900 text-white">
      </div>

      <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Login</button>
      
      <!-- Display success message -->
      <div v-if="successMessage" class="text-green-500">{{ successMessage }}</div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      successMessage: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          username: this.email,
          password: this.password,
        }, { withCredentials: true });

        // Dispatch the 'login' action to store the authentication token in Vuex
        this.$store.dispatch('login', response.data.access_token);

        // Save the token to localStorage
        localStorage.setItem('authToken', response.data.access_token);

        // Set success message
        this.successMessage = 'Login successful';

        // Redirect to the profile page after a brief delay (adjust as needed)
        setTimeout(() => {
          this.$router.push('/');
        }, 1000);

      } catch (error) {
        // Handle login error
        console.error('Login failed:', error.response.data.message);
        // Set an error property for display if needed
      }
    },
  },
};
</script>