<template>
  <div class="bg-gray-900 text-white min-h-screen py-6 sm:py-8 lg:py-12">
    <div class="max-w-md mx-auto mt-8">
      <h1 class="text-3xl font-semibold mb-6">Change Email</h1>

      <form @submit.prevent="changeEmail" class="mb-8">

        <label for="current_email" class="text-white block mb-2">Current Email:</label>
        <input v-model="currentEmail" type="email" name="current_email" required class="rounded-md px-4 py-2 w-full bg-gray-800 text-white mb-4">

        <label for="new_email" class="text-white block mb-2">New Email:</label>
        <input v-model="newEmail" type="email" name="new_email" required class="rounded-md px-4 py-2 w-full bg-gray-800 text-white mb-4">

        <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Change Email</button>
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
      user: {},
      currentEmail: '', // Add this line
      newEmail: '', // Add this line
      successMessage: '', // Add this line
    };
  },
  created() {
    // Fetch user profile data from the backend
    this.fetchUserProfile();
  },
  methods: {
    fetchUserProfile() {
      // Make API request to Flask backend for user profile
      axios.get('http://127.0.0.1:5000/profile', {
        headers: {
          Authorization: `Bearer ${this.$store.state.authToken}`,
        },
      })
        .then(response => {
          this.user = response.data;
          this.currentEmail = this.user.username; // Set currentEmail on fetch
        })
        .catch(error => {
          console.error('Error fetching user profile data:', error);
        });
    },
    async changeEmail() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/change-email', {
          current_email: this.currentEmail,
          new_email: this.newEmail,
        }, {
          headers: {
            Authorization: `Bearer ${this.$store.state.authToken}`,
          },
        });

        // Update local currentEmail on successful change
        this.currentEmail = this.newEmail;

        // Set success message and redirect
        this.successMessage = response.data.message;
        setTimeout(() => {
          this.$router.push('/profile'); // Redirect to the profile page
        }, 1000); // Redirect after 2 seconds (adjust as needed)

      } catch (error) {
        // Handle email change error
        console.error('Email change failed:', error.response.data.message);
        // Set an error property for display if needed
      }
    },
  },
};
</script>
