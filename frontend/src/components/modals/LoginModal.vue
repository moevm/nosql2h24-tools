<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div>
                <div :class="isRegistration ? 'active' : 'inactive'" class="login-block">
                <span @click="setRegistration" class="head">
                    Регистрация
                </span>
                </div>
                <div :class="isLogin ? 'active' : 'inactive'" class="login-block">
                    <span @click="setLogin"  class="head">Вход</span>
                    <button @click="closeModal">
                        <img src="../../assets/svg/close.svg" alt="close"/>
                    </button>
                </div>
            </div>
            <div class="form-block">
                <div v-if="isRegistration">
                    <form @submit.prevent="handleSubmit" novalidate>
                        <div>
                            <label for="username">Имя</label>
                            <input type="text" id="username" placeholder="Имя" v-model="form.name" required />
                        </div>
                        <div>
                            <label for="surname">Фамилия</label>
                            <input type="text" id="surname" placeholder="Фамилия" v-model="form.surname" required />
                        </div>
                        <div>
                            <label for="email">Электронная почта</label>
                            <input type="email" id="email" placeholder="Электронная почта" v-model="form.email" required />
                        </div>
                        <div  class="relative">
                            <label for="password">Пароль</label>
                            <input id="password" placeholder="Пароль" @focus="onFocusPassword"
                                   :type="isPasswordVisible ? 'text' : 'password'" v-model="form.password" required />
                            <button type="button" @click="isPasswordVisible = !isPasswordVisible" v-if="isPasswordInput"
                                    :class="isPasswordVisible ? 'opened-eye-button' : 'closed-eye-button'">
                                <img :src="isPasswordVisible ? openedEye : closedEye" alt="eye"/>
                            </button>
                        </div>
                        <div class="relative">
                            <label for="passwordConfirm">Повторите пароль</label>
                            <input id="passwordConfirm" placeholder="Повторите пароль" @focus="onFocusPasswordConfirm"
                                   :type="isPasswordConfirmVisible ? 'text' : 'password'" v-model="form.passwordConfirm" required />
                            <button type="button" @click="isPasswordConfirmVisible = !isPasswordConfirmVisible" v-if="isPasswordConfirmInput"
                                    :class="isPasswordConfirmVisible ? 'opened-eye-button' : 'closed-eye-button'">
                                <img :src="isPasswordConfirmVisible ? openedEye : closedEye" alt="eye"/>
                            </button>
                        </div>
                        <div class="checkbox-div">
                            <input type="checkbox" id="agreed" v-model="form.agreed" required />
                            <label for="agreed" class="checkbox-label"><u>Соглашаюсь с политикой обработки данных и<br>условиями предоставления товаров.</u></label>
                        </div>
                        <button type="submit">Зарегистрироваться</button>
                    </form>
                </div>
                <div v-if="isLogin">
                    <form @submit.prevent="handleSubmit" novalidate>
                        <div>
                            <label for="email">Электронная почта</label>
                            <input type="email" id="email" placeholder="Электронная почта" v-model="form.email" required />
                        </div>
                        <div  class="relative">
                            <label for="password">Пароль</label>
                            <input id="password" placeholder="Пароль" @focus="onFocusPassword"
                                   :type="isPasswordVisible ? 'text' : 'password'" v-model="form.password" required />
                            <button type="button" @click="isPasswordVisible = !isPasswordVisible"
                                    :class="isPasswordVisible ? 'opened-eye-button' : 'closed-eye-button'">
                                <img v-if="isPasswordInput" :src="isPasswordVisible ? openedEye : closedEye" alt="eye"/>
                            </button>
                        </div>
                        <button type="submit">Войти</button>
                    </form>
                </div>
            </div>
        </div>
        <UploadProgress v-if="isLoading"></UploadProgress>
    </div>
</template>

<script>
import { useToast } from "vue-toastification";

import closedEye from '../../assets/svg/eye/closedEye.svg'
import openedEye from '../../assets/svg/eye/openedEye.svg'
import {login, register} from "@/services/authService.js";
import UploadProgress from "@/components/UploadProgress.vue";

export default {
    components: {UploadProgress},
    setup() {
        const toast = useToast();
        return {toast}
    },
    data() {
        return {
            form: {
                name: '',
                surname: '',
                email: '',
                password: '',
                passwordConfirm: '',
                agreed: false,
            },
            isLogin: true,
            isRegistration: false,
            isPasswordInput: false,
            isPasswordConfirmInput: false,
            isPasswordVisible: false,
            isPasswordConfirmVisible: false,
            errors: '',
            isLoading: false,
            closedEye,
            openedEye
        }
    },
    props: {
        isVisible: {
            type: Boolean,
            required: true
        }
    },
    methods: {
        closeModal() {
            this.$emit('update:isVisible', false);
        },
        setRegistration() {
            this.isLogin = false
            this.isRegistration = true
        },
        setLogin() {
            this.isRegistration = false
            this.isLogin = true
        },
        onFocusPassword() {
            this.isPasswordInput = true
        },
        onFocusPasswordConfirm() {
            this.isPasswordConfirmInput = true
        },
        validate() {
            const emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
            if (!this.form.email) {
                this.errors += 'Email обязателен\n';
            } else if (!emailPattern.test(this.form.email)) {
                this.errors += 'Некорректный email\n';
            }
            if (!this.form.password) {
                this.errors += 'Пароль обязателен\n';
            } else if (this.form.password.length < 8) {
                this.errors += 'Пароль должен быть не менее 8 символов\n';
            }

            if (this.isRegistration) {
                if (!this.form.name) {
                    this.errors += 'Имя обязательно\n';
                }
                if (!this.form.surname) {
                    this.errors += 'Фамилия обязательна\n';
                }
                if (this.form.password !== this.form.passwordConfirm) {
                    this.errors += 'Пароли не совпадают\n';
                }
                if(!this.form.agreed) {
                    this.errors += 'Поставьте галочку, пожалуйста\n';
                }
            }
        },
        handleSubmit() {
            this.validate()
            if(this.errors){
                this.toast.error(this.errors)
                this.errors = ''
                return
            }
            this.isLoading = true
            if (this.isLogin) {
                login({
                        email: this.form.email,
                        password: this.form.password
                    }
                ).then((res) => {
                    this.isLoading = false
                    if (res === "SUCCESS") this.closeModal()
                })
            }
            if (this.isRegistration) {
                register({
                        name: this.form.name,
                        surname: this.form.surname,
                        email: this.form.email,
                        password: this.form.password
                    }
                ).then((res) => {
                    this.isLoading = false
                    if (res === "SUCCESS") this.closeModal()
                })
            }

        }
    }
};
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2000; /* Обеспечиваем, что модалка выше всего остального */
}

.modal-content {
    background: white;
    border-radius: 5px;
    min-width: 576px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.head {
    font-weight: bold;
    font-size: 26px;
    cursor: pointer;
}

.login-block {
    display:  inline-flex;
    justify-content: space-between;
    vertical-align: center;
    width: 50%;
    padding: 16px 32px;
}

.active {
    border-bottom: 2px  solid #6A983C;
}

.inactive {
    border-bottom: 2px  solid rgba(0, 0, 0, 0.20);
    color: rgba(0, 0, 0, 0.20);
}

.form-block {
    display: flex;
    flex-direction: column;
    padding-top: 32px;
    padding-bottom: 32px;
    align-items: center;
}

label {
    font-weight: 600;
    font-size: 14px;
    display: block;
    margin-bottom: 8px;
}

input[type="text"],
input[type="password"],
input[type="email"] {
    width: 384px;
    height: 42px;
    background-color: #F9F9F9;
    border: 1px solid #D1D1D1;
    border-radius: 12px;
    margin-bottom: 16px;
    padding-left: 21px;
    font-size: 14px;
}

input[type="checkbox"] {
    width: 32px;
    height: 32px;
    display: inline-block;
}

input[type="checkbox"]:checked {
    accent-color: #6A983C;
}

.checkbox-label {
    display: inline-block;
    font-weight: normal;
    color: #A9A9A9;
    margin-left: 14px;
    font-size: 13px;
}

.relative {
    position: relative;
}

.opened-eye-button {
    position: absolute;
    top: 37px;
    right: 14px;
    width: 20px;
    height: 20px;
}

.closed-eye-button {
    position: absolute;
    top: 42px;
    right: 14px;
    width: 20px;
    height: 20px;
}

.checkbox-div {
    margin-top: 16px;
}

button[type="submit"] {
    margin-top: 48px;
    height: 42px;
    width: 384px;
    border: 2px solid #46760A;
    border-radius: 12px;
    background-color: #6A983C;
    color: #FFFFFF;
    font-weight: 600;
}

</style>