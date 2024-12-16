import { createRouter, createWebHistory } from 'vue-router'

import {isUserAdmin, isUserAuthenticated} from "@/services/authService.js";
import HomeView from '@/views/HomeView.vue'
import AdminOrders from "@/views/admin/AdminOrders.vue";
import AdminEmployees from "@/views/admin/AdminEmployees.vue";
import AdminDashboard from "@/views/admin/AdminDashboard.vue";
import AdminReviews from "@/views/admin/AdminReviews.vue";
import AdminStatistics from "@/views/admin/AdminStatistics.vue";
import AdminTools from "@/views/admin/AdminTools.vue";
import AdminCategories from "@/views/admin/AdminCategories.vue";
import ProfileView from "@/views/profile/ProfileView.vue";
import MyRents from "@/views/profile/MyRents.vue";
import EditProfile from "@/views/profile/EditProfile.vue";
import ChangePassword from "@/views/profile/ChangePassword.vue";

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
    {
      path: '/profile/dashboard/:role',
      name: 'profile-dashboard',
      component: ProfileView,
      props: true,
      meta: {
        requiresLogin: true
      }
    },
    {
      path: '/profile/rents/:role',
      name: 'profile-rents',
      component: MyRents,
      props: true,
      meta: {
        requiresLogin: true
      }
    },
    {
      path: '/profile/edit/:role',
      name: 'profile-edit',
      component: EditProfile,
      props: true,
      meta: {
        requiresLogin: true
      }
    },
    {
      path: '/profile/change-password/:role',
      name: 'profile-change-password',
      component: ChangePassword,
      props: true,
      meta: {
        requiresLogin: true
      }
    },
  ],
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAdmin && !isUserAdmin()) {
    next({ name: 'home' });
  } else {
    next();
  }
  if (to.meta.requiresLogin && !isUserAuthenticated()){
    next({ name: 'home' });
  } else {
    next();
  }
});

export default router
