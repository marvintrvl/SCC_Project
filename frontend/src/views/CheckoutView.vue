<template>
  <div class="bg-gray-900 text-white min-h-screen py-6 sm:py-8 lg:py-12">
  <div class="max-w-md mx-auto mt-8">
    <h1 class="text-3xl font-bold mb-4">Checkout</h1>

    <div class="mb-4">
      <h2 class="text-2xl font-bold mb-2">Order Details</h2>
      <table class="border-collapse border border-gray-800 w-full">
        <thead>
          <tr class="bg-gray-800 text-white">
            <th class="py-2 px-4">Photo</th>
            <th class="py-2 px-4">Size</th>
            <th class="py-2 px-4">Quantity</th>
            <th class="py-2 px-4">Subtotal</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in cartItems" :key="item.id">
            <td class="py-2 px-4">{{ item.photo.name }}</td>
            <td class="py-2 px-4">{{ item.photo.size }}</td>
            <td class="py-2 px-4">{{ item.quantity }}</td>
            <td class="py-2 px-4">${{ item.photo.price }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p class="text-xl font-bold mb-2">Total: ${{ cartTotal }}</p>

    <div class="mb-4">
      <div class="border border-gray-800 p-4">
        <h2 class="text-2xl font-bold mb-2">Shipping Information</h2>
        <!-- Display user's shipping information -->
        <p><span class="font-bold">Name:</span> {{ user.first_name }} {{ user.last_name }}</p>
        <p><span class="font-bold">Street:</span> {{ user.street }}</p>
        <p><span class="font-bold">Postal Code:</span> {{ user.postal_code }}</p>
        <p><span class="font-bold">City:</span> {{ user.city }}</p>
        <p><span class="font-bold">Country:</span> {{ user.country }}</p>
      </div>
    </div>

    <div class="mb-4">
      <div class="border border-gray-800 p-4">
        <h2 class="text-2xl font-bold mb-2">Bank Information</h2>
        <!-- Allow the user to enter bank information -->
        <form @submit.prevent="placeOrder">
          <label for="bankInfo" class="block text-white mb-2">Enter Bank Information:</label>
          <textarea v-model="bankInfo" name="bankInfo" class="rounded-md px-4 py-2 w-full bg-gray-800 text-white resize-none" maxlength="30" rows="1" required></textarea>
          <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Place Order</button>
        </form>
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
        cartItems: [],
        cartTotal: 0,
        user: {},
        bankInfo: '',
      };
    },
    methods: {
      fetchCartItems() {
        axios.get('http://127.0.0.1:5002/get-cart', {
          headers: {
            Authorization: `Bearer ${this.$store.state.authToken}`,
          },
        })
          .then(response => {
            // Log raw API response 
            console.log('API Response:', response.data);

            const cartItems = response.data.cart_items;
            console.log('First Item:', cartItems[0]);
            const firstItem = cartItems[0];
            console.log('First item photo ID:', firstItem.photo_id);

            // Log cart items separately 
            console.log('Cart Items:', cartItems);

            this.cartItems = cartItems;
            this.cartTotal = response.data.total_price;
          })
          .catch(error => {
            console.error('Error fetching cart items:', error);
          });
      },
      fetchUserInfo() {
        axios.get('http://127.0.0.1:5000/profile', {
          headers: {
            Authorization: `Bearer ${this.$store.state.authToken}`,
          },
        })
          .then(response => {
            this.user = response.data;
          })
          .catch(error => {
            console.error('Error fetching user information:', error);
          });
      },
      placeOrder() {
        const orderDetails = this.cartItems.map(item => {
          if (item.photo) {
            return {
              quantity: item.quantity,
              size: item.photo.size,
              photo_name: item.photo.name,
              photo_id: item.photo_id,  // Corrected from item.photo_id
              subtotal: item.photo.price,
            };
          } else {
            console.error('Item photo is undefined:', item);
            return null;
          }
        }).filter(orderDetail => orderDetail !== null);

        const orderData = {
          total_price: this.cartTotal,
          shipping_address: `${this.user.street}, ${this.user.postal_code}, ${this.user.city}, ${this.user.country}`,
          bank_info: this.bankInfo,
          order_details: orderDetails,
          first_name: this.user.first_name,
          last_name: this.user.last_name,
        };

        axios.post('http://127.0.0.1:5004/place-order', orderData, {
          headers: {
            Authorization: `Bearer ${this.$store.state.authToken}`,
          },
        })
          .then(response => {
            console.log('Order placed successfully:', response.data);

            this.$router.push({
              name: 'OrderSuccessView',
              params: { orderId: response.data.order_id }
            });
            // Clear the user's cart after placing the order
            axios.delete('http://127.0.0.1:5002/clear-cart', {
              headers: {
                Authorization: `Bearer ${this.$store.state.authToken}`,
              },
            })
              .then(clearResponse => {
                console.log('Cart cleared successfully:', clearResponse.data);
                // Optionally, you can navigate to a thank you page or perform other actions
              })
              .catch(clearError => {
                console.error('Error clearing cart:', clearError);
                // Handle error while clearing the cart
              });
          })
          .catch(error => {
            console.error('Error placing order:', error);
            // Handle error, show a message to the user, etc.
          });
      },
    },

    created() {
      this.fetchCartItems();
      this.fetchUserInfo();
    },
  };
</script>


