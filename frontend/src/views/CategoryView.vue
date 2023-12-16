<template>
  <div class="bg-gray-900 text-white min-h-screen py-6 sm:py-8 lg:py-12">
    <div class="container mx-auto py-8">
      <h1 class="text-2xl font-bold text-center">{{ categoryTitle }}</h1>
      <p class="text-center">{{ categoryCount }} images in this category</p>
      <br>
      <div class="grid grid-cols-3 gap-4 mt-4">
        <div v-for="photo in photos" :key="photo.id">
          <router-link :to="'/photos/' + photo.id" class="group relative flex h-48 items-end overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-80">
            <img :src="photo.url" loading="lazy" :alt="photo.name" class="absolute inset-0 h-full w-full object-cover object-center transition duration-200 group-hover:scale-110" />
            <div class="pointer-events-none absolute inset-0 bg-gradient-to-t from-gray-800 via-transparent to-transparent opacity-50"></div>
            <span class="relative ml-4 mb-3 inline-block text-xs text-gray-300 md:ml-5 md:text-sm font-normal">{{ photo.name }}</span>
          </router-link>
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
      categoryTitle: '',
      categoryCount: 0,
      photos: [],
    };
  },
  watch: {
    '$route.params.categoryName'(newCategoryName) {
      // Watch for changes in the route parameters and refetch data
      this.fetchCategoryData(newCategoryName);
    },
  },
  created() {
    // Fetch category data based on initial route parameter
    const categoryName = this.$route.params.categoryName;
    this.fetchCategoryData(categoryName);
  },
  methods: {
    fetchCategoryData(categoryName) {
      // Make API request to Flask backend
      // Use the route /categories/<categoryName> to get category details
      axios.get(`http://127.0.0.1:5001/categories/${categoryName}`)
        .then(response => {
          const categoryData = response.data;
          this.categoryTitle = categoryData.category.name;
          this.categoryCount = categoryData.photos.length;
          this.photos = categoryData.photos.map(photo => ({
            id: photo.id,
            name: photo.name,
            url: `http://127.0.0.1:5001/${photo.image}`,
          }));
        })
        .catch(error => {
          console.error('Error fetching category data:', error);
        });
    },
  },
};
</script>
