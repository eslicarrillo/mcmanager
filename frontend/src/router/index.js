// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import DataViewer from '@/components/DataViewer.vue';

const routes = [
  {
    path: '/data-viewer',
    name: 'DataViewer',
    component: DataViewer
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
