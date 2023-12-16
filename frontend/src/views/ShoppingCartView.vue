<template>
  <div class="bg-gray-900 text-white min-h-screen py-6 sm:py-8 lg:py-12">
    <div class="max-w-3xl mx-auto mt-8">
      <h1 class="text-3xl font-semibold mb-6">Your Shopping Cart</h1>

      <form @submit.prevent="emptyCart">
        <button type="submit" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
          Empty Cart
        </button>
      </form>

      <table class="w-full border-collapse border border-gray-300 mt-4">
        <thead>
          <tr>
            <th class="p-2 border">Item</th>
            <th class="p-2 border">Size</th>
            <th class="p-2 border">Quantity</th>
            <th class="p-2 border">Subtotal</th>
            <th class="p-2 border">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in cartItems" :key="item.id" class="border-b">
            <td class="p-2 border">
              <div class="flex items-center">
                <div>
                  <p class="font-bold">{{ item.photo.name }}</p>
                  <p>{{ item.photo.title }}</p>
                </div>
                <img :src="item.photo.url" :alt="item.name" class="w-40 h-40 object-contain rounded-md ml-4">
              </div>
            </td>
            <td class="p-2 border">{{ item.photo.size }}</td>
            <td class="p-2 border">
              <form :id="'update-form-' + item.id" @submit.prevent="updateCartQuantity(item)">
                <input type="number" v-model="item.quantity" min="1">
                <button type="submit">Update</button>
              </form>
            </td>
            <td class="p-2 border">${{ item.photo.price }}</td>
            <td class="p-2 border">
              <button @click="deleteItem(item.id)" class="text-red-500 hover:text-red-700">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <p class="mt-4">Total: ${{ cartTotal }}</p>
      <br>
      <router-link to="/checkout" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Proceed to Checkout
      </router-link>
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
      cartItems: [],
    };
  },
  computed: {
    cartTotal() {
      return this.cartItems.reduce((total, item) => total + item.photo.price, 0);
    },
  },
  methods: {
    fetchCartItems() {
      axios.get('http://127.0.0.1:5002/get-cart', {
        headers: {
          Authorization: `Bearer ${this.$store.state.authToken}`,
        },
      })
      .then(response => {
        this.cartItems = response.data.cart_items;
        console.log(this.cartItems);
      })
      .catch(error => {
        console.error('Error fetching cart items:', error);
      });
    },
    emptyCart() {
      axios.delete('http://127.0.0.1:5002/clear-cart', {
        headers: {
          Authorization: `Bearer ${this.$store.state.authToken}`,
        },
      })
      .then(() => {
        this.cartItems = [];
        alert('Cart emptied successfully!');
      })
      .catch(error => {
        console.error('Error emptying cart:', error);
      });
    },
    updateCartQuantity(item) {
      const formData = new FormData();
      formData.append('quantity', item.quantity);

      axios.put(`http://127.0.0.1:5002/update-cart-item/${item.id}`, formData, {
        headers: {
          Authorization: `Bearer ${this.$store.state.authToken}`,
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(() => {
        // Refresh cart data after updating the quantity
        this.fetchCartItems();

        alert('Cart item quantity updated successfully!');
      })
      .catch(error => {
        console.error('Error updating cart item quantity:', error);
      });
    },
    deleteItem(itemId) {
      axios.delete(`http://127.0.0.1:5002/delete-cart-item/${itemId}`, {
        headers: {
          Authorization: `Bearer ${this.$store.state.authToken}`,
        },
      })
      .then(() => {
        // Remove the item directly from the Vue data
        this.cartItems = this.cartItems.filter(item => item.id !== itemId);
        alert('Item deleted from the cart successfully!');
      })
      .catch(error => {
        console.error('Error deleting item:', error);
      });
    },
  },
  created() {
    this.fetchCartItems();
  },
};
</script>

