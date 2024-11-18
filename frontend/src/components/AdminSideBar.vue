<template>
    <div>
        <button @click="toggleSidebar" class="toggle-button">
            <img src="../assets/svg/sidebar/right.svg" alt="no" :class="isOpen ? 'close-sidebar' : 'open-sidebar'"/>
        </button>


        <div class="sidebar" v-if="isOpen" :style="{ transform: isOpen ? 'translateX(0)' : 'translateX(-100%)' }">
            <router-link to="#">Информационная<br>панель</router-link> <br>
            <router-link to="#">Каталог</router-link><br>
            <router-link to="#">Сотрудники</router-link><br>
            <router-link to="#">Заказы</router-link><br>
            <router-link to="#">Отзывы</router-link><br>
            <router-link to="#">Статистика</router-link><br>
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
        openCatalogue() {
            this.isCatalogue = true
        }
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
    left: 0;
    width: 64px;
    height: 64px;
}

.close-sidebar {
    position: fixed;
    top: 50%;
    left: 218px;
    width: 64px;
    height: 64px;
    transform: rotate(180deg);
}
</style>