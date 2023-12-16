<!-- SearchResultsView.vue -->
<template>
    <div>
      <h2 class="text-3xl font-bold text-white mb-4">Search Results</h2>
      <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:gap-6 xl:gap-8">
        <!-- Display search results here -->
        <div v-for="(result, index) in searchResults" :key="index">
          <!-- Display each search result -->
          <router-link :to="`/photos/${result.id}`" class="group relative flex h-48 items-end overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-80">
            <img :src="result.url" loading="lazy" :alt="result.name" class="absolute inset-0 h-full w-full object-cover object-center transition duration-200 group-hover:scale-110" />
  
            <div class="pointer-events-none absolute inset-0 bg-gradient-to-t from-gray-800 via-transparent to-transparent opacity-50"></div>
  
            <span class="relative ml-4 mb-3 inline-block text-xs text-gray-300 md:ml-5 md:text-sm font-normal">{{ result.name }}</span>
          </router-link>
        </div>
      </div>
      <br>
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

    </div>
  </template>
  
  <script>
    import axios from 'axios';
  export default {
    props: {
      searchQuery: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        searchResults: [],
      };
    },
    mounted() {
      // Fetch search results using the searchQuery prop
      this.fetchSearchResults();
    },
    methods: {
      async fetchSearchResults() {
        try {
          const response = await axios.get(`http://127.0.0.1:5001/search?query=${this.searchQuery}`);
          this.searchResults = response.data.results;
        } catch (error) {
          console.error(error);
        }
      },
    },
  };
  </script>

