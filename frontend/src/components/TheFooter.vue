<script>
</script>

<template>
    <div class="footer">
        <div class="text">
            <p>© 2024</p>
            <p>Все права защищены</p>
            <p>ООО «Аренда инструментов»</p>
            <p>toolsrent@gmail.com</p>
            <p>+7 912 345 67 89</p>
        </div>
        <div class="links">
            <router-link to="/"><p>Условия аренды</p></router-link>
            <router-link to="/"><p>Контакты</p></router-link>
            <router-link to="/"><p>Оплата и доставка</p></router-link>
        </div>
    </div>

</template>

<style scoped>
.footer {
    width: 100%;
    height: 175px;
    background-color: #F9F9F9;
    padding: 32px;
    display: flex;
    justify-content: space-between;
}

.text p {
    font-size: 14px;
    font-weight: 400;
    margin-bottom: 8px;
}

.links p {
    font-size: 14px;
    font-weight: 400;
    margin-bottom: 16px;
    color: #6A983C;
}
</style>