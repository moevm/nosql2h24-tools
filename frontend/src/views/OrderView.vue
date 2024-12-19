<template>
    <UploadProgress v-if="isLoading" />
    <div class="main">
        <div class="header">
            <h1>Детали заказа</h1>
        </div>
        <div class="content">
            <div class="form">
                <div class="contacts">
                    <h3>Контактные данные</h3>
                    <div class="more-info">
                        <span>Ваши контактные данные</span>
                        <span>Шаг 1 из 4</span>
                    </div>
                    <div class="space-between mt-32">
                        <div class="contact-input">
                            <label for="name">Имя</label> <br />
                            <input type="text" id="name" v-model="profile.name" readonly/>
                        </div>
                        <div class="contact-input">
                            <label for="surname">Фамилия</label> <br />
                            <input type="text" id="surname" v-model="profile.surname" readonly/>
                        </div>
                    </div>
                    <div class="space-between mt-32">
                        <div class="contact-input">
                            <label for="email">Электронная почта</label> <br />
                            <input type="text" id="email" v-model="profile.email" readonly/>
                        </div>
                    </div>
                </div>
                <div class="getting mt-64">
                    <h3>Способ получения</h3>
                    <div class="more-info">
                        <span>Пожалуйста, выберите способ получения арендованных инструментов</span>
                        <span>Шаг 2 из 4</span>
                    </div>
                    <div class="mt-32">
                        <div class="check-form">
                            <div v-if="orderData.delivery_type !== 'at_pickup_point'" class="circle"></div>
                            <img v-else src="../assets/svg/radio-circle.svg" alt="checked"/>
                            <label>
                                <input type="radio" value="at_pickup_point" readonly/>
                                Самовывоз
                            </label>
                        </div>
                        <div class="check-form mt-16">
                            <div v-if="orderData.delivery_type !== 'to_door'" class="circle"></div>
                            <img v-else src="../assets/svg/radio-circle.svg" alt="checked"/>
                            <label>
                                <input type="radio" value="to_door" readonly />
                                Доставка
                            </label> <br />
                        </div>
                    </div>
                </div>
                <div class="payment mt-64">
                    <h3>Оплата</h3>
                    <div class="more-info">
                        <span>Пожалуйста, выберите способ оплаты</span>
                        <span>Шаг 3 из 4</span>
                    </div>
                    <div class="mt-32">
                        <div class="check-form">
                            <div v-if="orderData.payment_type !== 'cash'" class="circle"></div>
                            <img v-else src="../assets/svg/radio-circle.svg" alt="checked"/>
                            <label>
                                <input type="radio" value="cash" readonly />
                                Наличными (при получении)
                            </label>
                        </div>
                        <div class="check-form mt-16">
                            <div v-if="orderData.payment_type !== 'card'" class="circle"></div>
                            <img v-else src="../assets/svg/radio-circle.svg" alt="checked"/>
                            <label>
                                <input type="radio" value="card" readonly/>
                                Банковской картой
                            </label> <br />
                        </div>
                    </div>
                </div>
                <div class="confirm mt-64">
                    <h3>Подтверждение</h3>
                    <div class="more-info">
                        <span>Пожалуйста, поставьте галочку</span>
                        <span>Шаг 4 из 4</span>
                    </div>
                    <div class="check-form mt-32">
                        <img src="../assets/svg/checked.svg" alt="checked"/>
                        <label>
                            <input type="checkbox" readonly />
                            Я согласен с условиями аренды
                        </label>
                    </div>
                </div>
            </div>
            <div class="cart">
                <h2>Итоги заказа</h2>
                <div v-for="(item, index) in orderData.tools" :key="index" class="cart-item">
                    <div class="image-delete">
                        <div class="image">
                        </div>
                        <span class="delete" @click="">Оставить отзыв</span>
                    </div>
                    <div class="tool">
                        <p class="item-name">{{item.name}}</p>
                        <p class="item-type">Тип: {{item.type}}</p>
                        <p class="item-price">{{item.dailyPrice}} ₽</p>
                    </div>
                </div>
                <label for="start-date">Начальная дата:</label>
                {{getDate(orderData.start_leasing)}}
                <label for="end-date">Конечная дата:</label>
                {{getDate(orderData.end_leasing)}}
                <p class="total-sum">Итоговая стоимость: <span class="sum">{{orderData.price}}₽</span></p>

            </div>
        </div>
    </div>
</template>

<script>
import UploadProgress from "@/components/UploadProgress.vue";
import {getProfileData} from "@/services/profileServices.js";
import {useToast} from "vue-toastification";
import {getOrderData} from "@/services/orderServices.js";

export default {
    name: "OrderView",
    components: {UploadProgress},
    setup() {
        const toast = useToast()
        return {toast}
    },
    props: ['id'],
    data() {
        return {
            isLoading: true,
            orderData: {},
            profile: {}
        }
    },
    computed: {
    },
    beforeMount() {
        getOrderData(this.id).then((data) => {
            this.orderData = data
            console.log(data)
            getProfileData(data.client).then((newData) => {
                this.profile = newData
                this.isLoading = false
            })
        })
    },
    methods: {
        getDate(date) {
            if(date) return date.slice(0, 10)
        },
    }

}
</script>

<style scoped>
.main {
    width: 100%;
    padding: 32px;
}

.header {
    width: 100%;
    height: 60px;
    display: flex;
    align-items: flex-start;
    border-bottom: 1px solid #D5D5D5;
}

h1 {
    font-size: 32px;
    font-weight: bold;
}

.content {
    margin-top: 32px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.form {
    width: 754px;
}

h2 {
    font-size: 26px;
    font-weight: bold;
}

.cart {
    width: 431px;
    padding: 16px 32px;
    border-radius: 10px;
    border: 1px solid #D5D5D5;
}

.cart-item {
    margin-top: 32px;
    display: flex;
    flex-direction: row;
}

.image {
    width: 100px;
    height: 64px;
    background-color: #F9F9F9;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 15px;
}

.tool {
    margin-left: 16px;
}

.item-name {
    font-size: 15px;
}

.item-type {
    font-size: 12px;
    margin-top: 5px;
}

.item-price {
    font-size: 18px;
    font-weight: bold;
    color: #6A983C;
    margin-top: 39px;
}

.delete {
    margin-left: 16px;
    font-size: 12px;
    cursor: pointer;
}

.cart label {
    display: block;
    margin-top: 10px;
}
.cart input {
    margin-top: 5px;
}

.data-error {
    color: red;
    margin-top: 8px;
}

.total-sum {
    margin-top: 32px;
    font-size: 16px;
    font-weight: bold;
}

.sum {
    margin-left: 8px;
    font-size: 24px;
    color: #6A983C;
}

h3 {
    font-size: 22px;
    font-weight: bold;
}

.mt-64 {
    margin-top: 64px;
}

.mt-32 {
    margin-top: 32px;
}

.mt-16 {
    margin-top: 16px;
}

.more-info {
    margin-top: 8px;
    display: flex;
    justify-content: space-between;
    width: 100%;
    color: #A9A9A9;
    font-size: 12px;
}

.space-between {
    display: flex;
    justify-content: space-between;
}

label {
    font-size: 14px;
    font-weight: 600;
}

.contacts input {
    margin-top: 8px;
    width: 360px;
    height: 42px;
    background-color: #F9F9F9;
    border: 1px solid #D1D1D1;
    border-radius: 12px;
    padding-left: 22px;
}

.circle {
    width: 20px;
    height: 20px;
    border-radius: 10px;
    border: 1px solid #D1D1D1;
    background-color: #FFFFFF;
    display: inline-block;
}

.square {
    width: 20px;
    height: 20px;
    border-radius: 3px;
    border: 1px solid #D1D1D1;
    background-color: #FFFFFF;
    display: inline-block;
}

.check-form {
    width: 754px;
    height: 48px;
    background-color: #F9F9F9;
    border-radius: 12px;
    border: 1px solid #D1D1D1;
    display: flex;
    align-items: center;
    padding-left: 18px;
}

.check-form label {
    margin-left: 16px;
}

.check-form img {
    width: 20px;
    height: 20px;
}

input[type="checkbox"]{
    display: none;
}

.check-order {
    margin-top: 64px;
    width: 316px;
    height: 56px;
    border: 2px solid #46760A;
    background-color: #6A983C;
    border-radius: 12px;
    color: white;
    font-size: 16px;
    font-weight: bold;
}
</style>