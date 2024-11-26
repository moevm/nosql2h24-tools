<template>
    <div>
        <div class="overlay" v-if="isOpen">
            <div class="sidebar" :style="{ transform: isOpen ? 'translateX(0%)' : 'translateX(100%)'}">
                <div class="header">
                    <span>Добавить новый инструмент</span>
                    <img src="../../assets/svg/close.svg" @click="closePanel" alt="close" />
                </div>
                <div class="content">
                    <form @submit.prevent="handleSubmit" novalidate>
                        <div>
                            <label for="name">Название инструмента</label>
                            <input type="text" id="name" placeholder="Название инструмента" v-model="form.name" class="width-input" required />
                        </div>
                        <div>
                            <label for="dailyPrice">Цена за аренду на 1 день</label>
                            <input type="number" id="dailyPrice" placeholder="Цена за аренду на 1 день" v-model="form.dailyPrice" class="width-input" required />
                        </div>
                        <div>
                            <label for="totalPrice">Цена инструмента</label>
                            <input type="number" id="totalPrice" placeholder="Цена инструмента" v-model="form.totalPrice" class="width-input" required />
                        </div>
                        <div class="mb-16">
                            <label for="image">Изображения инструмента</label>
                            <input type="file" accept="image/*" @change="onFileChange" multiple/>
                            <div v-if="form.images.length">
                                <img v-for="(image, index) in form.images"
                                     :src="image"
                                     :key="index"
                                     alt="Uploaded Image"
                                     class="uploaded-image"
                                />
                            </div>
                        </div>
                        <div>
                            <label for="feature">Характеристика инструмента</label>
                            <input type="text" id="feature" placeholder="Характеристика" v-model="tempFeature" class="width-input" required />
                            <label for="featureValue">Значение характеристики инструмента</label>
                            <input type="text" id="featureValue" placeholder="Значение характеристики" v-model="tempFeatureValue" class="width-input" required />
                            <ul>
                                <li class="image-li" v-for="([key, value], index) in Object.entries(form.features)" :key="index">
                                    {{ key }}: {{ value }}
                                </li>
                            </ul>
                            <button type="button" @click="addFeature" class="add-img-btn">Добавить характеристику</button>
                        </div>
                        <div>
                            <label for="category-select">Категория</label>
                            <select id="category-select" v-model="form.category">
                                <option v-for="category in categories" :value="category">{{ category.name }}</option>
                            </select>
                            <div v-if="form.category.types">
                                <label for="type-select">Тип</label>
                                <select id="type-select" v-model="form.type">
                                    <option v-for="type in form.category.types" :value="type.name">{{ type.name }}</option>
                                </select>
                            </div>
                        </div>
                        <div>
                            <label for="description">Описание инструмента</label>
                            <input type="text" id="description" placeholder="Описание инструмента" v-model="form.description" class="width-input" required />
                        </div>
                        <button type="submit">Добавить новый инструмент</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {addNewTool, addNewType} from "@/services/adminServices.js";
import {useToast} from "vue-toastification";

export default {
    name: "AddNewTool",
    props: {
        isOpen: {
            type: Boolean,
            default: false,
        },
        categories: {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            errors: "",
            tempFeature: "",
            tempFeatureValue: "",
            form: {
                name: "",
                dailyPrice: 0,
                totalPrice: 0,
                images: [],
                features: {},
                category: "",
                type: "",
                description: ""
            },
        };
    },
    setup() {
        const toast = useToast()
        return {toast}
    },
    methods: {
        closePanel() {
            this.$emit('close');
        },
        onFileChange(event) {
            const files = event.target.files;
            this.form.images = []
            for (let i = 0; i < files.length; i++) {
                const file = files[i]
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.form.images.push(e.target.result); // Сохранение base64 строки
                };
                reader.readAsDataURL(file);
            }
        },
        addFeature() {
            if (this.tempFeature !== "" && this.tempFeatureValue !== ""){
                this.form.features[this.tempFeature] = this.tempFeatureValue
                this.tempFeature = ""
                this.tempFeatureValue = ""
            }
        },
        validate() {
            this.form.category = this.form.category.name
            if (this.form.name === "") {
                this.errors += "Название инструмента не должно быть пустым!\n"
            }
            if (this.form.dailyPrice === 0){
                this.errors += "Установите цену за аренду инструмента!\n"
            }
            if (this.form.totalPrice === 0){
                this.errors += "Укажите цену данного инструмента!\n"
            }
            if (this.form.category === ""){
                this.errors += "Выберите категорию для данного инструмента!\n"
            }
            if (this.form.type === ""){
                this.errors += "Выберите тип для данного инструмента!\n"
            }
            if (this.form.description === ""){
                this.errors += "Добавьте описание для данного инструмента!\n"
            }
        },
        handleSubmit() {
            this.validate()
            if (this.errors) {
                this.toast.error(this.errors)
                this.errors = ""
                return
            }
            this.isLoading = true
            addNewTool(this.form).then((res) => {
                this.isLoading = false
                if (res === "SUCCESS")
                    this.closePanel()
            })
        }
    }
}
</script>


<style scoped>
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); /* полупрозрачный черный */
    z-index: 4000; /* ниже, чем панель */
}

.sidebar {
    z-index: 5000;
    position: fixed;
    top: 0;
    right: 0;
    width: 500px; /* Ширина боковой панели */
    height: 100vh;
    background-color: #FFFFFF;
    box-shadow: 2px 0 5px rgba(0,0,0,0.5);
    transition: transform 0.5s;
}

.header {
    width: 100%;
    height: 86px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.2);
    display: flex;
    align-items: center;
}

.header span {
    font-size: 24px;
    font-weight: bold;
    margin-left: 32px;
}

.header img {
    cursor: pointer;
    margin-left: 32px;
}

label {
    font-weight: 600;
    font-size: 14px;
    display: block;
    margin-bottom: 8px;
}

select,
.width-input {
    width: 384px;
    height: 42px;
    background-color: #F9F9F9;
    border: 1px solid #D1D1D1;
    border-radius: 12px;
    margin-bottom: 16px;
    padding-left: 21px;
    font-size: 14px;
}

.content {
    width: 100%;
    height: calc(100vh - 86px - 32px);
    padding: 48px 64px 32px;
    overflow-y: auto;
}

.image-li {
    width: 384px;
    height: auto;
    background-color: #FAFAFA;
    border: 1px solid #D1D1D1;
    border-radius: 6px;
}

.add-img-btn {
    width: auto;
    height: 32px;
    background-color: #A1DA68;
    border-radius: 8px;
    border: 2px solid #6A983C;
    margin-bottom: 16px;
    padding: 16px;
    display: flex;
    align-items: center;
}

.mb-16 {
    margin-bottom: 16px;
}

.uploaded-image {
    width: 200px;
    margin: 16px 0;
}

button[type="submit"] {
    background-color: #6A983C;
    border: 2px solid #46760A;
    color: white;
    font-size: 16px;
    font-weight: bold;
    border-radius: 12px;
    width: 300px;
    height: 48px;
    margin-left: 48px;
    margin-top: 16px;
}
</style>