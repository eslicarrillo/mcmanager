<!-- src/App.vue -->
<template>
  <div id="app">
    <nav>
      <router-link to="/data-viewer">Visor de Datos</router-link>
    </nav>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
/* Añade estilos según sea necesario */
</style>
