import { createStore } from 'vuex';

const store = createStore({
  state: {
    isAuthenticated: false,
    isAdmin: false,
  },
  mutations: {
    login(state) {
      state.isAuthenticated = true;
    },
    logout(state) {
      state.isAuthenticated = false;
    },
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    isAdmin: (state) => state.isAdmin,
  },
});

export default store;