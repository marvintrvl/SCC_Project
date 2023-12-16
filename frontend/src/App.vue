<template>
  <div id="app">
    <NavbarView />
    <FooterView />
    <router-view />
  </div>
</template>

<script>
import NavbarView from './components/NavbarView.vue';

export default {
  components: {
    NavbarView,
  },
};
</script>