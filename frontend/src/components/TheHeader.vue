<script>
import LoginModal from "@/components/modals/LoginModal.vue";
import store from "@/js/store.js";
import {mapGetters} from "vuex";
import {logoutUser} from "@/services/authService.js";

export default {
    components: {LoginModal},
    data() {
        return {
            showLoginModal: false,
            searchForm: {
                text: "",
            },
        }
    },
    computed: {
        ...mapGetters(['isAuthenticated', 'isAdmin']), // Подключаем геттеры
    },

    methods: {
        openLogin() {
            this.showLoginModal = true
        },
        logout() {
            store.dispatch('logout')
            logoutUser()
        },
        handleSubmit() {

        }
    }
}
</script>

<template>
    <div class="header">
        <div class="content">
            <router-link to="/">
                <img src="../assets/svg/logo.svg" alt="logo"/>
            </router-link>
            <div class="search">
                <form @submit.prevent="handleSubmit" novalidate>
                    <input type="search" v-model="searchForm.text" placeholder="Поиск инструмента..."/>
                    <button><img src="../assets/svg/search.svg" alt="search"/></button>
                </form>
            </div>
            <div class="profile-basket">
                <button v-if="!isAuthenticated">
                    <img src="../assets/svg/profile.svg" alt="profile" @click="openLogin"/>
                </button>
                <router-link v-if="isAuthenticated" to="/profile/dashboard">
                    <img src="../assets/svg/profile.svg" alt="profile"/>
                </router-link>
                <button>
                    <img src="../assets/svg/basket.svg" alt="basket"/>
                </button>
            </div>
        </div>
    </div>
    <LoginModal :isVisible="showLoginModal" @update:isVisible="showLoginModal = $event"></LoginModal>
</template>

<style scoped>
.header {
    width: 100%;
    position: sticky;
    top: 0;
    background-color: #FFFFFF;
    z-index: 1000;
}

.content {
    height: 106px;
    margin: 0 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.search form {
    width: 500px;
    height: 42px;
    background-color: #F9F9F9;
    border-radius: 12px;
    border: 1px solid #D1D1D1;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.profile-basket {
    width: 88px;
    height: 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

select {
    margin-left: 16px;
    font-size: 15px;
    font-weight: bold;
    width: 130px;
}

input[type="search"]{
    margin-left: 24px;
    width: 262px;
}

form button {
    width: 16px;
    height: 16px;
    margin-right: 24px;
}
</style>