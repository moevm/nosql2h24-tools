<template>
    <div>
        <button @click="toggleSidebar" class="toggle-button">
            <img src="../assets/svg/sidebar/right.svg" alt="no" class="sidebar-button" :class="isOpen ? 'close-sidebar' : 'open-sidebar'"/>
        </button>


        <div class="sidebar" :style="{ transform: isOpen ? 'translateX(0)' : 'translateX(-100%)'}">
            <div class="link" :class="{ active: isActive('/admin/dashboard') }">
                <router-link to="/admin/dashboard">
                    <p>Информационная<br>панель</p>
                </router-link>
            </div>
            <div class="link" :class="{ active: isActive('/admin/tools') }">
                <router-link to="/admin/tools">
                    <p>Инструменты</p>
                </router-link>
            </div>
            <div class="link" :class="{ active: isActive('/admin/categories') }">
                <router-link to="/admin/categories">
                    <p>Категории и типы</p>
                </router-link>
            </div>
            <div class="link" :class="{ active: isActive('/admin/employees') }">
                <router-link to="/admin/employees">
                    <p>Сотрудники</p>
                </router-link>
            </div>
            <div class="link" :class="{ active: isActive('/admin/orders') }">
                <router-link to="/admin/orders">
                    <p>Заказы</p>
                </router-link>
            </div>
            <div class="link" :class="{ active: isActive('/admin/reviews') }">
                <router-link to="/admin/reviews">
                    <p>Отзывы</p>
                </router-link>
            </div>
            <div class="link" :class="{ active: isActive('/admin/statistics') }">
                <router-link to="/admin/statistics">
                    <p>Статистика</p>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'AdminSideBar',
    data() {
        return {
            isOpen: false,
            isCatalogue: false,
        };
    },
    methods: {
        toggleSidebar() {
            this.isOpen = !this.isOpen;
        },
        isActive(route) {
            return this.$route.path === route;
        },

    }
};
</script>

<style scoped>
.sidebar {
    z-index: 5000;
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 250px; /* Ширина боковой панели */
    background-color: #FFFFFF;
    color: white;
    padding: 10px;
    box-shadow: 2px 0 5px rgba(0,0,0,0.5);
    transition: transform 0.5s;
}
.toggle-button {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 10000;
}
.close-button {
    color: black;
    margin-top: 20px;
}

.open-sidebar {
    position: fixed;
    top: 50%;
    transform: translateX(-25%);
    width: 64px;
    height: 64px;
}

.close-sidebar {
    position: fixed;
    top: 50%;
    transform: translateX(310%) rotate(180deg);
    width: 64px;
    height: 64px;
}

.sidebar-button {
    transition: transform 0.5s;
}

.link {
    border-left: 3px solid rgba(0, 0, 0, 0.2);
    padding: 8px 16px;
}

.link p {
    color: black;
}

.link.active {
    border-left: 3px solid #6A983C;
}

</style>