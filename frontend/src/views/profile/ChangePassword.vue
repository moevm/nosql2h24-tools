<template>
    <UploadProgress v-if="isLoading"  />
    <main>
        <ProfileSideBar :role="role"/>
        <div class="content">
            <h2>Изменить пароль</h2>
            <form @submit.prevent="handleSubmit" novalidate>
                <div class="password">
                    <label for="password">Текущий пароль</label> <br/>
                    <input id="password" type="password" placeholder="Текущий пароль" v-model="form.current_password" required/>
                </div>
                <div class="password">
                    <label for="new-password">Текущий пароль</label> <br/>
                    <input id="new-password" type="password" placeholder="Новый пароль" v-model="form.new_password" required/>
                </div>
                <div class="password">
                    <label for="confirm-password">Подтвердите пароль</label> <br/>
                    <input id="confirm-password" type="password" placeholder="Подтвердите пароль" v-model="confirmPassword" required/>
                </div>
                <div class="button-container">
                    <button type="submit" :disabled="isButtonDisabled">
                        Обновить пароль
                    </button>
                </div>

            </form>

        </div>
    </main>
</template>

<script>
import ProfileSideBar from "@/components/ProfileSideBar.vue";
import UploadProgress from "@/components/UploadProgress.vue";
import {changePassword} from "@/services/profileServices.js";
import {useToast} from "vue-toastification";
import {changeAdminPassword} from "@/services/adminProfileServices.js";

export default {
    name: "ChangePassword",
    components: {UploadProgress, ProfileSideBar},
    props: ['role'],
    setup() {
        const toast = useToast();
        return {toast}
    },
    data(){
        return {
            isLoading: false,
            confirmPassword: "",
            form: {
                current_password: "",
                new_password: "",
            }

        }
    },
    computed: {
        isButtonDisabled() {
            return !this.form.current_password || !this.form.new_password || !this.confirmPassword
        },
    },
    methods: {
        handleSubmit() {
            if(this.form.new_password !== this.confirmPassword){
                this.toast.error("Введенные пароли не совпадают!")
                return
            }
            this.isLoading = true
            if(this.role === 'client'){
                changePassword(this.form).then((res) => {
                    this.isLoading = false
                })
            } else {
                changeAdminPassword(this.form).then((res) => {
                    this.isLoading = false
                })
            }

        }
    },
}
</script>

<style scoped>
main {
    padding: 32px 64px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.content{
    width: 879px;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    padding: 32px 64px;
}

h2 {
    font-weight: 600;
    font-size: 20px;
}

.password {
    margin-top: 32px;
}

label {
    font-size: 16px;
    color: #575757;
}

input {
    margin-top: 8px;
}

input[type="password"] {
    width: 350px;
    padding: 11px 24px;
    background-color: #F9F9F9;
    border: 1px solid #D1D1D1;
    border-radius: 12px;
}

.button-container {
    margin-top: 48px;
    display: flex;
    flex-direction: row-reverse;
}

form button {
    width: 194px;
    padding: 16px;
    background-color: #6A983C;
    color: #FFFFFF;
    font-weight: bold;
    border-radius: 12px;
    border: 2px solid #46760A;
}

form button[disabled] {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
}
</style>