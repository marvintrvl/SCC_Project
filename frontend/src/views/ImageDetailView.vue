<template>
  <div class="bg-gray-900 text-white min-h-screen py-6 sm:py-8 lg:py-12">
    <div class="photo-detail flex justify-center items-center px-4">
      <div class="w-1/2 pr-8">
        <img :src="photo.url" :alt="photo.name" class="w-2/3 h-auto rounded-md">
      </div>

      <!-- Wrap the form in a div and reduce its size by 50% -->
      <div class="w-1/4 pl-8"> <!-- Adjusted width to 1/4 -->
        <h1 class="text-2xl font-bold mb-2">{{ photo.name }}</h1>
        <form @submit.prevent="addToCart" class="mt-2">
          <label for="size" class="block text-sm font-medium text-gray-700">Select Size:</label>
          <select v-model="selectedSize" name="size" id="size" class="mt-1 p-2 border rounded-md w-full">
            <option v-for="sizeOption in sizeOptions" :key="sizeOption.value" :value="sizeOption.value">
              {{ sizeOption.label }}
            </option>
          </select>

          <label for="quantity" class="block text-sm font-medium text-gray-700 mt-2">Quantity:</label>
          <input v-model="selectedQuantity" type="number" name="quantity" min="1" class="mt-1 p-2 border rounded-md w-full">

          <button type="submit" class="mt-2 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
            Add to Cart
          </button>
        </form>
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
import { mapState } from 'vuex';

export default {
  data() {
    return {
      photo: {},
      selectedSize: 'S',
      selectedQuantity: 1,
      sizeOptions: [
        { label: 'Small (20 cm) - $20', value: 'S' },
        { label: 'Medium (40 cm) - $40', value: 'M' },
        { label: 'Large (60 cm) - $60', value: 'L' },
      ],
    };
  },
  computed: {
    ...mapState(['authToken']),
  },
  mounted() {
    this.fetchPhotoDetails();
  },
  methods: {
    fetchPhotoDetails() {
      const photoId = this.$route.params.id;
      axios.get(`http://127.0.0.1:5001/photos/${photoId}`)
        .then(response => {
          this.photo = {
            ...response.data.photo,
            name: response.data.photo.name,
            url: `http://127.0.0.1:5001/${response.data.photo.image || ''}`
          };
        })
        .catch(error => {
          console.error('Error fetching photo details:', error);
        });
    },
    addToCart() {
      const photoId = this.photo.id;
      const token = this.authToken;

      axios.post(`http://localhost:5002/add-to-cart/${photoId}`, {
        photoId: this.photo.id,
        size: this.selectedSize,
        quantity: this.selectedQuantity,
        name: this.photo.name,
        url: this.photo.url,
      }, 
      { headers: { Authorization: `Bearer ${token}` },
        withCredentials: true, 
      }
    )
        .then(() => {
          this.$store.dispatch('fetchCart');
          alert('Added to cart!');
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
};
</script>
