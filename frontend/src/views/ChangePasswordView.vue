<template>
  <div class="bg-gray-900 text-white min-h-screen py-6 sm:py-8 lg:py-12">
    <div class="max-w-md mx-auto mt-8">
      <h1 class="text-3xl font-semibold mb-6">Change Password</h1>

      <form @submit.prevent="changePassword" class="mb-8">
        <label for="current_password" class="text-white block mb-2">Current Password:</label>
        <input v-model="currentPassword" type="password" name="current_password" required class="rounded-md px-4 py-2 w-full bg-gray-800 text-white mb-4">

        <label for="new_password" class="text-white block mb-2">New Password:</label>
        <input v-model="newPassword" type="password" name="new_password" required class="rounded-md px-4 py-2 w-full bg-gray-800 text-white mb-4">

        <label for="repeat_password" class="text-white block mb-2">Repeat New Password:</label>
        <input v-model="repeatPassword" type="password" name="repeat_password" required class="rounded-md px-4 py-2 w-full bg-gray-800 text-white mb-4">

        <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Change Password</button>
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
      currentPassword: '',
      newPassword: '',
      repeatPassword: '',
      successMessage: '', // Add this line
    };
  },
  methods: {
    changePassword() {
      // Make API request to Flask backend to change password
      axios.post('http://127.0.0.1:5000/change-password', {
        currentPassword: this.currentPassword,
        newPassword: this.newPassword,
        repeatPassword: this.repeatPassword,
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
          console.error('Error changing password:', error);
        });
    },
  },
};
</script>
