<template>
    <UploadProgress v-if="isLoading" />
    <div class="content">
        <div class="image">
            <img v-if="tool.images[currentImage]" :src="tool.images[currentImage]" alt=""/>
            <button class="left-button image-button" @click="onImageChange(-1)">
                <img src="../assets/svg/image_buttons/left_button.svg" alt="prev" />
            </button>
            <button class="right-button image-button" @click="onImageChange(1)">
                <img src="../assets/svg/image_buttons/right_button.svg" alt="next" />
            </button>
        </div>
        <div class="info">
            <h1>{{tool.name}}</h1>
            <div class="mt-16">
                <template v-for="i in range(tool.rating)">
                    <img src="../assets/svg/stars/black_star.svg" alt="star" />
                </template>
                <template v-for="i in range(5 - tool.rating)">
                    <img src="../assets/svg/stars/star.svg" alt="star" />
                </template>
            </div>
            <div class="line"></div>
            <div class="price">
                <span>Цена за сутки: {{tool.dailyPrice}}₽</span>
                <span class="ml-32">Катория: {{tool.category}}</span>
                <p class="mt-16">Тип: {{tool.type}}</p>
            </div>
            <div class="features">
                <h2>Характеристики:</h2>
                <div v-for="(value, key) in tool.features" :key="key" class="feature">
                    <span>{{key}}</span>
                    <span>{{value}}</span>
                </div>
            </div>
            <div class="description">
                <div class="desc-header" :style="isDescription ?
                'border-bottom: 3px solid #6A983C' : 'border-bottom: 3px solid #D5D5D5'">
                    <h2 class="cursor-pointer" @click="isDescription = true">Описание</h2>
                </div>
                <div class="desc-header" :style="!isDescription ?
                'border-bottom: 3px solid #6A983C' : 'border-bottom: 3px solid #D5D5D5'">
                    <h2 class="cursor-pointer" @click="isDescription = false">Отзывы</h2>
                </div>
            </div>
            <div v-if="isDescription" class="mt-16">
                {{tool.description}}
            </div>
            <div v-else class="mt-16">
                <template v-if="reviews">
                    <div v-for="(review, index) in reviews" :key="index" class="review">
                        <div class="review-header">
                            <div class="reviewer">
                                <img src="../assets/svg/reviewer.svg" alt="reviewer"/>
                                <div class="ml-16">
                                    <span>{{review.reviewer_surname}}</span>
                                    <span>{{review.reviewer_name}}</span>
                                    <div class="stars">
                                        <template v-for="i in range(review.rating)">
                                            <img src="../assets/svg/stars/black_star.svg" alt="star" />
                                        </template>
                                        <template v-for="i in range(5 - review.rating)">
                                            <img src="../assets/svg/stars/star.svg" alt="star" />
                                        </template>
                                    </div>
                                </div>
                            </div>
                            <span class="date">{{review.date}}</span>
                        </div>
                        <div class="mt-16">
                            {{review.text}}
                        </div>
                    </div>
                </template>
            </div>
            <div class="center">
                <button class="add-to-cart" @click="handleAddToCart">
                    Добавить в корзину
                </button>
            </div>

        </div>
    </div>
</template>

<script>
import {getToolDetails} from "@/services/toolServices.js";
import UploadProgress from "@/components/UploadProgress.vue";
import {useToast} from "vue-toastification";
import {getToolReviews} from "@/services/reviewServices.js";

export default {
    name: "ToolView",
    components: {UploadProgress},
    setup() {
        const toast = useToast();
        return {toast}
    },
    data() {
        return {
            isLoading: true,
            tool: {},
            currentImage: 0,
            isDescription: true,
            reviews: [],
        }
    },
    computed: {
        id() {
            return this.$route.params.id
        },
    },
    watch: {
        '$route.params.search': {
            immediate: true,
            handler(newId) {
                this.fetchResults(newId);
            },
        }
    },
    beforeMount() {
        this.fetchResults()
    },
    methods: {
        getDate(date) {
            return date.slice(0, 10)
        },
        fetchResults() {
            getToolDetails(this.id).then((data) => {
                this.tool = data
                this.isLoading = false
                getToolReviews(this.id).then((newData) => {
                    this.reviews = newData
                })
            })
        },
        onImageChange(num) {
            if(this.tool.images[this.currentImage + num]) {
                this.currentImage += num
            }
        },
        range(num) {
            return Array.from({ length: num }, (v, k) => k)
        },
        handleAddToCart() {
            const isAuthenticated = localStorage.getItem('isAuthenticated')
            if(!isAuthenticated){
                this.toast.error("Инструмент не добавлен!\n Пожалуйста, войдите сначала в свой аккаунт!")
                return
            }
            const isAdmin = localStorage.getItem('isAdmin')
            if(isAdmin){
                this.toast.error("Работники не могут делать заказы!")
                return
            }
            const cart = this.getCart()
            cart.push(this.tool)
            this.updateCartInLocalStorage(cart)
            this.toast.success("Инструмент успешно добавлен в корзину!")
        },
        getCart() {
            const cart = localStorage.getItem('cart')
            if(cart){
                return JSON.parse(cart)
            } else {
                return []
            }
        },
        updateCartInLocalStorage(cart) {
            localStorage.setItem('cart', JSON.stringify(cart));
        },
    }
}
</script>



<style scoped>
.content {
    width: 100%;
    padding: 32px;
    display: flex;
    justify-content: space-between;
}

.image {
    width: 540px;
    height: 540px;
    background-color: #D9D9D9;
    position: relative;
    display: flex; /* Используем Flexbox */
    align-items: center; /* Вертикальное центрирование */
    justify-content: space-between; /* Распределяем пространство между кнопками */
}

.image-button {
    background: transparent; /* Убираем фон кнопок */
    border: none; /* Убираем рамку */
    cursor: pointer; /* Указываем, что кнопки кликабельны */
}

.left-button, .right-button {
    position: absolute; /* Позволяет разместить кнопки в фиксированных позициях */
}

.left-button {
    left: 10px; /* Отступ от левого края */
}

.right-button {
    right: 10px; /* Отступ от правого края */
}

.info {
    width: 612px;
}

h1 {
    font-size: 32px;
    font-weight: 600;
}

.stars img {
    width: 20px;
    height: 20px;
    margin-right: 2px;
}

.line {
    width: 100%;
    height: 1px;
    background-color: #D5D5D5;
    margin-top: 16px;
}

.price {
    margin-top: 32px;
    font-size: 18px;
    font-weight: 600;
}

.ml-32 {
    margin-left: 32px;
}

.mt-16 {
    margin-top: 16px;
}

.ml-16 {
    margin-left: 16px;
}

.features {
    margin-top: 32px;
}

h2 {
    font-size: 18px;
    font-weight: 600;
}

.feature {
    width: 100%;
    height: 32px;
    margin-top: 8px;
    display: flex;
    justify-content: space-between;
    padding-left: 16px;
    padding-right: 16px;
    align-items: center;
    border: 1px solid #D5D5D5;
    border-radius: 10px;
}

.description {
    margin-top: 32px;
}

.desc-header {
    display: inline-block;
    width: 50%;
    height: 40px;
}

.cursor-pointer {
    cursor: pointer;
}

.review {
    width: 100%;
    border: 1px solid #D5D5D5;
    border-radius: 12px;
    padding: 16px;
    margin-top: 16px;
}

.review-header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.reviewer {
    display: flex;
    flex-direction: row;
    align-items: center;
}

.add-to-cart {
    width: 448px;
    height: 48px;
    background-color: #6A983C;
    border-radius: 12px;
    border: 2px solid #46760A;
    color: white;
    font-size: 20px;
    font-weight: bold;
}

.center {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 32px;
}
</style>