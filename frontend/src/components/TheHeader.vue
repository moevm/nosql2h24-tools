<script>
export default {
    name: 'HeaderComp',
    methods: {
        openRegistrationModal() {
            return 0
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
                <button>
                    <img src="../assets/svg/profile.svg" alt="profile"/>
                </button>
                <button>
                    <img src="../assets/svg/basket.svg" alt="basket" @click="openRegistrationModal"/>
                </button>

            </div>
        </div>
    </div>
</template>

<style scoped>
.header {
    width: 100%;
    border-bottom: 1px solid rgba(0, 0, 0, 0.2);
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