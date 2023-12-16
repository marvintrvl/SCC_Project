<template>
  <div class="bg-gray-900 text-white min-h-screen py-6 sm:py-8 lg:py-12">
    <form @submit.prevent="register" class="max-w-md mx-auto mt-8">
      <div class="mb-4">
        <label for="first_name" class="text-white block mb-2">First Name:</label>
        <input v-model="first_name" id="first_name" name="first_name" class="rounded-md px-4 py-2 w-full bg-gray-800 text-white">
      </div>
  
      <div class="mb-4">
        <label for="last_name" class="text-white block mb-2">Last Name:</label>
        <input v-model="last_name" id="last_name" name="last_name" class="rounded-md px-4 py-2 w-full bg-gray-800 text-white">
      </div>
  
      <div class="mb-4">
        <label for="email" class="text-white block mb-2">Email:</label>
        <input v-model="email" id="email" name="email" type="email" class="rounded-md px-4 py-2 w-full bg-gray-800 text-white">
      </div>
  
      <div class="mb-4">
        <label for="password" class="text-white block mb-2">Password:</label>
        <input v-model="password" id="password" name="password" type="password" class="rounded-md px-4 py-2 w-full bg-gray-800 text-white">
      </div>
  
      <div class="mb-4">
        <label for="street" class="text-white block mb-2">Street:</label>
        <input v-model="street" id="street" name="street" class="rounded-md px-4 py-2 w-full bg-gray-800 text-white">
      </div>
  
      <div class="mb-4">
        <label for="city" class="text-white block mb-2">City:</label>
        <input v-model="city" id="city" name="city" class="rounded-md px-4 py-2 w-full bg-gray-800 text-white">
      </div>
  
      <div class="mb-4">
        <label for="postal_code" class="text-white block mb-2">Postal Code:</label>
        <input v-model="postal_code" id="postal_code" name="postal_code" class="rounded-md px-4 py-2 w-full bg-gray-800 text-white">
      </div>
  
      <div class="mb-4">
        <label for="country" class="text-white block mb-2">Country:</label>
        <input v-model="country" id="country" name="country" class="rounded-md px-4 py-2 w-full bg-gray-800 text-white">
      </div>
  
      <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Register</button>

      <!-- Display success and error messages -->
      <div v-if="successMessage" class="text-green-500">{{ successMessage }}</div>
      <div v-if="error" class="text-red-500">{{ error }}</div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      street: '',
      city: '',
      postal_code: '',
      country: '',
      error: null,
      successMessage: '', // Add this line
    };
  },
  methods: {
    async register() {
      try {
        await axios.post('http://127.0.0.1:5000/register', {
          first_name: this.first_name,
          last_name: this.last_name,
          username: this.email,
          password: this.password,
          street: this.street,
          city: this.city,
          postal_code: this.postal_code,
          country: this.country,
        }, { withCredentials: true });

        // Set success message
        this.successMessage = 'Registration successful';

        // Redirect to the login page after a brief delay (adjust as needed)
        setTimeout(() => {
          this.$router.push('/login');
        }, 1000);

      } catch (error) {
        // Handle registration error
        console.error('Registration failed:', error.response.data.message);
        this.error = error.response.data.message; // Set an error property for display
      }
    },
  },
};
</script>