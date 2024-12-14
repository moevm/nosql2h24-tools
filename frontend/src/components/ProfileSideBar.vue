<template>
    <div class="sidebar">
        <div :class="{ active: isActive('/profile/dashboard') }">
            <router-link to="/profile/dashboard">
                <p>
                    Мой профиль
                </p>
            </router-link>
        </div>
        <div :class="{ active: isActive('/profile/rents') }">
            <router-link to="/profile/rents">
                <p>
                    Мои аренды
                </p>
            </router-link>
        </div>
        <div :class="{ active: isActive('/profile/edit') }">
            <router-link to="/profile/edit">
                <p>
                    Редактировать профиль
                </p>
            </router-link>
        </div>
        <div :class="{ active: isActive('/profile/change-password') }">
            <router-link to="/profile/change-password">
                <p>
                    Изменить пароль
                </p>
            </router-link>
        </div>
        <div @click="logoutUser">
            <p>
                Выйти
            </p>
        </div>
    </div>
</template>

<script>
import {logoutUser} from "@/services/authService.js";

export default {
    name: "ProfileSideBar",
    methods: {
        logoutUser,
        isActive(route) {
            return this.$route.path === route;
        }
    }
}
</script>

<style scoped>
.sidebar {
    display: flex;
    flex-direction: column;
}

.sidebar div {
    padding: 8px;
    border-left: 3px solid rgba(0, 0, 0, 0.2);
}

.sidebar div.active {
    border-left: 3px solid #6A983C;
}

p {
    margin-left: 8px;
    cursor: pointer;
    color: black;
    font-size: 16px;
}
</style>