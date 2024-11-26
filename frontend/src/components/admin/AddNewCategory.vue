<template>
    <div>
        <div class="overlay" v-if="isOpen">
            <div class="sidebar" :style="{ transform: isOpen ? 'translateX(0%)' : 'translateX(100%)'}">
                <div class="header">
                    <span>Добавить новую категорию</span>
                    <img src="../../assets/svg/close.svg" @click="closePanel" alt="close" />
                </div>
                <div class="content">
                    <form @submit.prevent="handleSubmit" novalidate>
                        <div>
                            <label for="name">Название категории</label>
                            <input type="text" id="name" placeholder="Название категории" v-model="form.name" required />
                        </div>
                        <button type="submit">Добавить новую категорию</button>
                    </form>
                </div>

            </div>
        </div>
        <UploadProgress v-if="isLoading"></UploadProgress>
    </div>
</template>

<script>
import {addNewCategory} from "@/services/adminServices.js";
import UploadProgress from "@/components/UploadProgress.vue";
import {useToast} from "vue-toastification";
export default {
    name: "AddNewCategory",
    components: {UploadProgress},
    props: {
        isOpen: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            form: {
                name: "",
            },
            errors: "",
            isLoading: false,
        };
    },
    setup() {
        const toast = useToast();
        return {toast}
    },
    methods: {
        closePanel() {
            this.$emit('close');
        },
        validate() {
            if(this.form.name === "") {
                this.errors += "Название категории не должно быть пустым!\n"
            }
        },
        handleSubmit() {
            this.validate()
            if(this.errors) {
                this.toast.error(this.errors)
                this.errors = ""
                return
            }
            this.isLoading = true
            addNewCategory(this.form).then((res) => {
                this.isLoading = false
                if (res === "SUCCESS")
                    this.closePanel()
            })
        },
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
    height: 100vh;
    width: 500px; /* Ширина боковой панели */
    background-color: #FFFFFF;
    box-shadow: 2px 0 5px rgba(0,0,0,0.5);
    transition: transform 0.5s;
}

.header {
    width: 100%;
    height: 10%;
    border-bottom: 1px solid rgba(0, 0, 0, 0.2);
    display: flex;
    align-items: center;
}

.header span {
    font-size: 24px;
    font-weight: bold;
    margin-left: 64px;
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

input[type="text"],
input[type="number"] {
    width: 372px;
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
    height: 700px;
    padding: 48px 64px 32px;
}

form {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
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
}
</style>