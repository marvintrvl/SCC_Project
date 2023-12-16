<template>
  <div class="bg-gray-900 text-white min-h-screen py-6 sm:py-8 lg:py-12">
    <div class="max-w-md mx-auto mt-8">
      <h1 class="text-3xl font-semibold mb-6">Change Address</h1>

      <form @submit.prevent="changeAddress" class="mb-8">
        <label for="new_street" class="text-white block mb-2">New Street:</label>
        <input v-model="newStreet" type="text" name="new_street" required class="rounded-md px-4 py-2 w-full bg-gray-800 text-white mb-4">

        <label for="new_city" class="text-white block mb-2">New City:</label>
        <input v-model="newCity" type="text" name="new_city" required class="rounded-md px-4 py-2 w-full bg-gray-800 text-white mb-4">

        <label for="new_postal_code" class="text-white block mb-2">New Postal Code:</label>
        <input v-model="newPostalCode" type="text" name="new_postal_code" required class="rounded-md px-4 py-2 w-full bg-gray-800 text-white mb-4">

        <label for="new_country" class="text-white block mb-2">New Country:</label>
        <input v-model="newCountry" type="text" name="new_country" required class="rounded-md px-4 py-2 w-full bg-gray-800 text-white mb-4">

        <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Change Address</button>
      </form>

      <!-- Display success message -->
      <div v-if="successMessage" class="text-green-500">{{ successMessage }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      newStreet: '',
      newCity: '',
      newPostalCode: '',
      newCountry: '',
      successMessage: '', // Add this line
    };
  },
  methods: {
    changeAddress() {
      // Make API request to Flask backend to change address
      axios.post('http://127.0.0.1:5000/change-address', {
        newStreet: this.newStreet,
        newCity: this.newCity,
        newPostalCode: this.newPostalCode,
        newCountry: this.newCountry,
      }, {
        headers: {
          Authorization: `Bearer ${this.$store.state.authToken}`,
        },
      })
        .then(response => {
          // Set success message and redirect
          this.successMessage = response.data.message;
          setTimeout(() => {
            this.$router.push('/profile'); // Redirect to the profile page
          }, 1000); // Redirect after 2 seconds (adjust as needed)
        })
        .catch(error => {
          // Handle error, e.g., display an error message
          console.error('Error changing address:', error);
        });
    },
  },
};
</script>
