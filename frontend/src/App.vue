<script setup>
import { RouterLink, RouterView } from 'vue-router';
import Header from "./components/TheHeader.vue";
import Footer from "./components/TheFooter.vue"
import {computed, onBeforeMount} from 'vue';
import AdminSideBar from "@/components/AdminSideBar.vue";
import store from "@/js/store.js";
import {isUserAdmin} from "@/services/authService.js";


</script>

<template>
    <div class="app-container">
        <Header />
        <AdminSideBar v-if="store.state.isAdmin" />
        <main class="content">
            <RouterView />
        </main>
        <Footer />
    </div>

</template>

<style scoped>
.content {
    min-height: 100vh;
}
</style>
