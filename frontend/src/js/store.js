import { createStore } from 'vuex';

const store = createStore({
  state: {
    isAuthenticated: false,
    isAdmin: false,
  },
  mutations: {
    login(state) {
      state.isAuthenticated = true;
      state.isAdmin = localStorage.getItem('isAdmin') === 'true';
    },
    logout(state) {
      state.isAuthenticated = false;
      state.isAdmin = false;
    },
    setAdmin(state, isAdmin) {
      state.isAdmin = isAdmin;
    },
    setAuthentication(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated;
    },
  },
  actions: {
    login({ commit }) {
      commit('login'); // Вызываем мутацию login
    },
    logout({ commit }) {
      commit('logout'); // Вызываем мутацию logout
    },
    checkLocalStorage({ commit }) {
      const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
      const isAdmin = localStorage.getItem('isAdmin') === 'true';

      commit('setAuthentication', isAuthenticated);
      commit('setAdmin', isAdmin);
    },
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    isAdmin: (state) => state.isAdmin,
  },
});

export default store;