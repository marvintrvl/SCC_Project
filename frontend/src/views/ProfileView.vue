<template>
  <div class="bg-gray-900 text-white min-h-screen py-6 sm:py-8 lg:py-12">
  <div class="container mx-auto py-8">
    <div class="max-w-md mx-auto mt-8 bg-gray-800 p-6 rounded-md shadow-md">
      <h1 class="text-3xl font-semibold mb-6 text-white">Welcome, {{ user.first_name }}!</h1>

      <div class="mb-8">
        <h2 class="text-xl font-semibold mb-4 text-white">Your Profile Details:</h2>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-gray-400">First Name:</p>
            <p class="text-white">{{ user.first_name }}</p>
          </div>
          <div>
            <p class="text-gray-400">Last Name:</p>
            <p class="text-white">{{ user.last_name }}</p>
          </div>
          <div>
            <p class="text-gray-400">Email:</p>
            <p class="text-white">{{ user.username }}</p>
          </div>
          <div>
            <p class="text-gray-400">Street:</p>
            <p class="text-white">{{ user.street }}</p>
          </div>
          <div>
            <p class="text-gray-400">City:</p>
            <p class="text-white">{{ user.city }}</p>
          </div>
          <div>
            <p class="text-gray-400">Postal Code:</p>
            <p class="text-white">{{ user.postal_code }}</p>
          </div>
          <div>
            <p class="text-gray-400">Country:</p>
            <p class="text-white">{{ user.country }}</p>
          </div>
        </div>
      </div>

      <div>
        <h2 class="text-xl font-semibold mb-4 text-white">Actions:</h2>
        <ul>
          <router-link to="/change-email" class="text-blue-500"><li>Change Email</li></router-link>
          <router-link to="/change-password" class="text-blue-500"><li>Change Password</li></router-link>
          <router-link to="/change-name" class="text-blue-500"><li>Change Name</li></router-link>
          <router-link to="/change-address" class="text-blue-500"><li>Change Address</li></router-link>
          <router-link to="/view-orders" class="text-blue-500"><li>View Orders</li></router-link>
        </ul>
      </div>
    </div>
  </div>
  <br>
 </div>
<footer class="py-4 bg-gray-800 flex flex-col justify-center items-center">
      <div class="flex justify-center items-center mb-4">
        <a class="hover:text-gray-300" href="https://www.instagram.com/marvin.trvl">Contact Us</a>
        <span class="mx-2 text-gray-400">|</span>
        <a class="hover:text-gray-300" href="https://www.instagram.com/marvin.trvl">Impressum</a>
        <span class="mx-2 text-gray-400">|</span>
        <a class="hover:text-gray-300" href="https://www.instagram.com/marvin.trvl">Instagram</a>
      </div>
      <div class="text-gray-400">&copy; 2023 SnapStock Licensing & Prints</div>
    </footer>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: {},
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

          // Log the fetched user data
          console.log('Fetched user data:', this.user);
        })
        .catch(error => {
          console.error('Error fetching user profile data:', error);
        });
    },
  },
};
</script>
