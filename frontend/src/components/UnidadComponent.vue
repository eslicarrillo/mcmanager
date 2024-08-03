<template>
  <div>
    <h1>Unidades</h1>
    <ul>
      <li v-for="unidad in unidades" :key="unidad.id">{{ unidad.name }}</li>
    </ul>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'UnidadComponent',
  computed: {
    ...mapState(['unidades']),
  },
  mounted() {
    this.fetchUnidades();
  },
  methods: {
    ...mapActions(['fetchUnidades']),
  },
};
</script>

<style scoped>
/* Añade estilos aquí */
</style>
