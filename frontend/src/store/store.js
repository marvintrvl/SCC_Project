import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state: {
    authToken: localStorage.getItem('authToken') || null,
    cartItems: [],
  },
  mutations: {
    setAuthToken(state, token) {
      state.authToken = token;
    },
    clearAuthToken(state) {
      state.authToken = null;
    },
    setCart(state, cartItems) {
      state.cartItems = cartItems;
    },
    updateCartItems(state, updatedItems) {
      state.cartItems = updatedItems;
    },
  },
  actions: {
    fetchCart({ commit, state }) {
      const token = state.authToken;

      axios.get('http://127.0.0.1:5002/get-cart', { headers: { Authorization: `Bearer ${token}` } })
        .then(response => {
          commit('setCart', response.data.cart_items);
        })
        .catch(error => {
          console.error('Error fetching cart items:', error);
        });
    },
    login({ commit }, token) {
      commit('setAuthToken', token);
      // Save the token to localStorage
      localStorage.setItem('authToken', token);
    },
    logout({ commit }) {
      commit('clearAuthToken');
      // Remove the token from localStorage
      localStorage.removeItem('authToken');
    },
    updateCart({ commit, state }, updatedItems) {
      const token = state.authToken;
      console.log('Updated Cart Items:', updatedItems);

      // Make an API call to update the cart on the server
      axios.put('http://127.0.0.1:5002/update-cart', { cart_items: updatedItems }, {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then(response => {
          console.log('Cart updated successfully:', response.data);
          commit('updateCartItems', updatedItems);
        })
        .catch(error => {
          console.error('Error updating cart:', error);
        });
    },
  },
});

export default store;
