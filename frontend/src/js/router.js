import { createRouter, createWebHistory } from 'vue-router'

import {isUserAdmin} from "@/services/authService.js";
import HomeView from '@/views/HomeView.vue'
import AdminOrders from "@/views/admin/AdminOrders.vue";
import AdminEmployees from "@/views/admin/AdminEmployees.vue";
import AdminDashboard from "@/views/admin/AdminDashboard.vue";
import AdminReviews from "@/views/admin/AdminReviews.vue";
import AdminStatistics from "@/views/admin/AdminStatistics.vue";
import AdminTools from "@/views/admin/AdminTools.vue";
import AdminCategories from "@/views/admin/AdminCategories.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/admin/orders',
      name:'admin-orders',
      component: AdminOrders,
      meta: {
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/employees',
      name:'admin-employees',
      component: AdminEmployees,
      meta: {
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/dashboard',
      name:'admin-dashboard',
      component: AdminDashboard,
      meta: {
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/reviews',
      name:'admin-reviews',
      component: AdminReviews,
      meta: {
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/statistics',
      name:'admin-statistics',
      component: AdminStatistics,
      meta: {
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/tools',
      name:'admin-tools',
      component: AdminTools,
      meta: {
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/categories',
      name:'admin-categories',
      component: AdminCategories,
      meta: {
        requiresAdmin: true,
      },
    },
  ],
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAdmin && !isUserAdmin()) {
    next({ name: 'home' });
  } else {
    next();
  }
});

export default router
