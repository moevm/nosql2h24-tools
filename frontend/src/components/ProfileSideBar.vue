<template>
    <div class="sidebar">
        <div :class="{ active: isActive('/profile/dashboard') }">
            <router-link :to="{name: 'profile-dashboard', props: {role: role}}">
                <p>
                    Мой профиль
                </p>
            </router-link>
        </div>
        <div v-if="role === 'client'" :class="{ active: isActive('/profile/rents') }">
            <router-link :to="{name: 'profile-rents', props: {role: role}}">
                <p>
                    Мои аренды
                </p>
            </router-link>
        </div>
        <div :class="{ active: isActive('/profile/edit') }">
            <router-link :to="{name: 'profile-edit', props: {role: role}}">
                <p>
                    Редактировать профиль
                </p>
            </router-link>
        </div>
        <div :class="{ active: isActive('/profile/change-password') }">
            <router-link :to="{name: 'profile-change-password', props: {role: role}}">
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
    props: {
      role: {
          type: String,
          default: "client"
      }
    },
    methods: {
        logoutUser,
        isActive(route) {
            return this.$route.path.startsWith(route);
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