<script setup>

</script>

<template>
    <div class="navbar">
        <div class="elem">
            <span class="text">Категории </span>
            <img src="../assets/svg/dot.svg" alt="dot" class="dot"/>
        </div>
        <div class="elem">
            <span class="text">Чаще всего арендуют</span>
            <img src="../assets/svg/dot.svg" alt="dot" class="dot"/>
        </div>
        <div class="elem">
            <span class="text">Отзывы</span>
            <img src="../assets/svg/dot.svg" alt="dot" class="dot"/>
        </div>
        <div class="elem">
            <span class="text">Условия аренды</span>
            <img src="../assets/svg/dot.svg" alt="dot" class="dot"/>
        </div>
        <div class="elem">
            <span class="text">Оплата и доставка</span>
            <img src="../assets/svg/dot.svg" alt="dot" class="dot"/>
        </div>
        <div class="elem">
            <span class="text">Контакты</span>
            <img src="../assets/svg/dot.svg" alt="dot" class="dot"/>
        </div>
    </div>
</template>

<style scoped>
.navbar {
    position: sticky;
    top: 106px;
    z-index: 1000;
    display: flex;
    align-items: center;
    padding: 0 48px;
    width: 100%;
    height: 64px;
    background-color: #F9F9F9;
    justify-content: space-between;
}

.text {
    font-size: 15px;
    font-weight: 600;
}

.elem {
    display: flex;
    align-items: center;
}

.dot {
    margin-left: 2px;
}
</style>