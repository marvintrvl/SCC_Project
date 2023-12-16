<template>
  <div class="bg-gray-900 text-white min-h-screen py-6 sm:py-8 lg:py-12">
    <div class="max-w-md mx-auto mt-8 bg-green-500 p-6 rounded-md shadow-md">
      <h1 class="text-3xl font-semibold mb-4 text-white">Your order has been placed successfully!</h1>

      <div v-if="order">
        <div class="mt-6">
          <h2 class="text-xl font-semibold mb-2 text-white">Order Details:</h2>
          <p class="text-white"><span class="font-bold">Order ID:</span> #{{ order.id }}</p>
          <p class="text-white"><span class="font-bold">Date:</span> {{ order.date_created }}</p>
          <p class="text-white"><span class="font-bold">Total Amount:</span> ${{ order.total_price }}</p>
        </div>

        <div class="mt-8">
          <p class="text-white">Thank you for your purchase. We appreciate your business.</p>

          <!-- Additional order details -->
          <p class="text-white mt-4">
            To complete your order, please transfer the total amount of ${{ order.total_price }} to the following German IBAN within 7 days:
          </p>

          <p class="text-white font-bold mt-2">DE89370400440532013000</p>

          <p class="text-white mt-4">
            Please include your order ID (#{{ order.id }}) as the payment reference.
          </p>

          <p class="text-white mt-4">
            Your order will be processed and shipped once we receive the payment. If we don't receive the payment within 7 days, the order will be canceled.
          </p>
          <br>
        </div>

        <!-- "Take me Home" button -->
        <router-link to="/" class="text-white block bg-blue-800 hover:bg-gray-700 py-2 px-4 rounded text-center">Take me Home</router-link>
      </div>

      <div v-else>
        <p class="text-white">Order details not available.</p>
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
      order: null,
    };
  },

  methods: {
    fetchOrderDetails(orderId) {
      axios.get(`http://127.0.0.1:5004/get-order/${orderId}`, {
        headers: {
          Authorization: `Bearer ${this.$store.state.authToken}`,
        },
      })
        .then(response => {
          console.log('API Response:', response.data);
          this.order = response.data;
        })
        .catch(error => {
          console.error('Error fetching order details:', error);
        });
    },
  },

  created() {
    // Get order ID from route param
    const orderId = this.$route.params.orderId; 
    this.fetchOrderDetails(orderId);
  }
};
</script>
