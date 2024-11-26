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
        }
    },
    computed: {
        ...mapGetters(['isAuthenticated', 'isAdmin']), // Подключаем геттеры
    },

    methods: {
        openProfile() {
            this.showLoginModal = true
        },
        logout() {
            store.dispatch('logout')
            logoutUser()
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
                Поиск
            </div>
            <div class="profile-basket">
                <button v-if="!isAuthenticated">
                    <img src="../assets/svg/profile.svg" alt="profile" @click="openProfile"/>
                </button>
                <button v-if="isAuthenticated" @click="logout">
                    Выйти
                </button>
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

.search {
    width: 500px;
    height: 42px;
    background-color: #F9F9F9;
}

.profile-basket {
    width: 88px;
    height: 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>