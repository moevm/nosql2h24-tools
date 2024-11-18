<script setup>
import { RouterLink, RouterView } from 'vue-router';
import Header from "./components/TheHeader.vue";
import Footer from "./components/TheFooter.vue"
import { computed } from 'vue';
import { useStore } from 'vuex';
import AdminSideBar from "@/components/AdminSideBar.vue";

const store = useStore();
const isAdmin = computed(() => store.getters.isAdmin);
</script>

<template>
    <div class="app-container">
        <Header />
        <AdminSideBar v-if="isAdmin" />
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
