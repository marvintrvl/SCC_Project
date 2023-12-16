<template>
    <div class="bg-gray-900 text-white min-h-screen py-6 sm:py-8 lg:py-12">
    <div class="max-w-md mx-auto mt-8">
      <h1 class="text-3xl font-semibold mb-6">My Orders</h1>
  
      <div v-if="orders.length === 0">
        <p class="text-gray-500">No orders yet.</p>
      </div>
  
      <div v-else>
        <div v-for="order in orders" :key="order.id" class="border rounded-md p-8 mb-8">
          <h2 class="text-xl font-semibold mb-4">Order #{{ order.id }} - Total: ${{ order.total_price }}</h2>
          <ul>
            <li v-for="item in order.details" :key="item.id" class="flex justify-between items-center mb-4">
              <div class="flex-1">
                <div>
                  {{ item.quantity }} x {{ item.photo_name }} ({{ item.size }})
                </div>
                <div class="text-gray-500">
                  Subtotal: ${{ item.subtotal }}
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        orders: [],
      };
    },
  
    created() {
      axios
        .get('http://127.0.0.1:5004/view-orders', {
          headers: {
            Authorization: `Bearer ${this.$store.state.authToken}`,
          },
        })
        .then((res) => {
          this.orders = res.data;
        });
    },
  };
  </script>