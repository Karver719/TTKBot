import { createRouter, createWebHistory } from 'vue-router';
import App from '../App.vue';
import Login from '../components/Login.vue';
import Tables from '../components/Tables.vue'; // Создайте этот компонент

const routes = [
  { path: '/', component: Login },
  { path: '/tables', component: Tables, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('adminToken');
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next('/');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;