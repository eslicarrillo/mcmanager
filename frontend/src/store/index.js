import { createStore } from 'vuex';
import axios from 'axios';  // Asegúrate de importar axios

export default createStore({
  state: {
    unidades: [],
  },
  mutations: {
    setUnidades(state, unidades) {
      state.unidades = unidades;
    },
  },
  actions: {
    fetchUnidades({ commit }) {
      axios.get('/unidades/')
        .then(response => {
          commit('setUnidades', response.data);
        });
    },
  },
  modules: {
    // Define tus módulos aquí
  },
});
