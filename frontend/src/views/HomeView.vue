<template>
  <div class="bg-gray-900 text-white min-h-screen py-6 sm:py-8 lg:py-12">
    <!-- Welcome Message -->
    <div class="text-center mb-6 md:mb-8">
      <p class="text-xl text-white md:text-2xl font-bold">
        Welcome to SnapStock Licensing & Prints! We offer licenses, prints, and calendars of high-quality images.
      </p>
    </div>

    <!-- Search Bar -->
    <form @submit.prevent="search" class="mb-6 text-center">
      <input v-model="searchKeywords" type="text" placeholder="Search for keywords" class="p-2 border rounded-md">
      <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Search</button>
    </form>

    <!-- Latest Photos -->
    <div class="mb-4 flex items-center justify-between gap-8 sm:mb-8 md:mb-12">
      <div class="flex items-center gap-12">
        <h2 class="text-3xl font-bold text-white lg:text-4xl">Latest Photos</h2>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:gap-6 xl:gap-8">
      <div v-for="(picture, index) in recentPictures" :key="index">
        <router-link :to="`/photos/${picture.id}`" class="group relative flex h-48 items-end overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-80">
          <img :src="picture.url" loading="lazy" :alt="picture.name" class="absolute inset-0 h-full w-full object-cover object-center transition duration-200 group-hover:scale-110" />

          <div class="pointer-events-none absolute inset-0 bg-gradient-to-t from-gray-800 via-transparent to-transparent opacity-50"></div>

          <span class="relative ml-4 mb-3 inline-block text-xs text-gray-300 md:ml-5 md:text-sm font-normal">{{ picture.name }}</span>
        </router-link>
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
      recentPictures: []
    };
  },
  async mounted() {
    try {
      const response = await axios.get('http://127.0.0.1:5001/');

      // Generate image URLs correctly
      this.recentPictures = response.data.pictures
        .filter(p => p.url) // Filter out photos with undefined URLs
        .map(p => {
          return {
            ...p,
            url: `http://127.0.0.1:5001${p.url.replace('/images', '') || ''}` // Use full URL in Vue
          };
        });

    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async search() {
      // Navigate to the SearchResultsView with the search query
      this.$router.push({ name: 'search-results', params: { query: this.searchKeywords } });
    },
  },
};
</script>