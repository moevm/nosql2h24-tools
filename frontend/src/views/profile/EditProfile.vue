<template>
    <UploadProgress v-if="isLoading"  />
    <main>
        <ProfileSideBar :role="role" />
        <div class="content">
            <h2>Редактировать профиль</h2>
            <form @submit.prevent="handleSubmit" novalidate>
                <div class="image-loader">
                    <label for="image">Загрузите новое изображение профиля</label> <br/>
                    <input type="file" accept="image/png, image/jpeg" id="image" @change="onFileChange">
                </div>
                <div class="img-container">
                    <img v-if="form.newImage"
                         :src="form.newImage"
                         alt="image"
                         class="img"
                    />
                    <div v-else class="no-image"></div>
                </div>
                <div class="name-surname">
                    <div class="name">
                        <label for="name">Имя</label> <br/>
                        <input type="text" id="name" v-model="form.newName" />
                    </div>
                    <div class="surname">
                        <label for="surname">Фамилия</label> <br/>
                        <input type="text" id="surname" v-model="form.newSurname" />
                    </div>
                </div>
                <div class="name-surname">
                    <div class="phone">
                        <label for="phone">Телефон</label>
                        <input type="text" id="phone" v-model="form.newPhone">
                    </div>
                    <div class="email">
                        <label for="email">Электронная почта</label> <br/>
                        <input type="text" id="email" :placeholder="profile.email" readonly>
                    </div>
                </div>

                <div class="button-container">
                    <button type="submit" :disabled="isButtonDisabled">
                        Обновить данные
                    </button>
                </div>

            </form>

        </div>
    </main>
</template>

<script>
import ProfileSideBar from "@/components/ProfileSideBar.vue";
import UploadProgress from "@/components/UploadProgress.vue";
import {getProfileData, updateProfileData} from "@/services/profileServices.js";
import {getAdminProfileData, updateAdminProfileData} from "@/services/adminProfileServices.js";

export default {
    name: "EditProfile",
    components: {UploadProgress, ProfileSideBar},
    props: ['role'],
    data(){
        return {
            isLoading: true,
            profile: {},
            form: {
                newImage: "",
                newName: "",
                newSurname: "",
                newPhone: "",
            }

        }
    },
    beforeMount() {
        if(this.role === 'client') {
            getProfileData().then((data) => {
                this.profile = data
                this.form.newName = data.name
                this.form.newSurname = data.surname
                this.form.newImage = data.image
                this.form.newPhone = data.phone
                this.isLoading = false
            })
        }
        else {
            getAdminProfileData().then((data) => {
                this.profile = data
                this.form.newName = data.name
                this.form.newSurname = data.surname
                this.form.newImage = data.image
                this.form.newPhone = data.phone
                this.isLoading = false
            })
        }
    },
    computed: {
        isButtonDisabled() {
            return (this.form.newImage === this.profile.image
                && this.form.newName === this.profile.name
                && this.form.newSurname === this.profile.surname
                && this.form.newPhone === this.profile.phone)
                || !this.form.newName || !this.form.newSurname
                || (this.form.newPhone && !this.profile.phone)
        },
    },
    methods: {
        onFileChange(event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) => {
                this.form.newImage = e.target.result; // Сохранение base64 строки
            };
            reader.readAsDataURL(file);
        },
        handleSubmit() {
            this.isLoading = true
            const data = {}
            if(this.form.newImage !== this.profile.image){
                data.image = this.form.newImage
            }
            if(this.form.newName !== this.profile.name){
                data.name = this.form.newName
            }
            if(this.form.newSurname !== this.profile.surname){
                data.surname = this.form.newSurname
            }
            if(this.form.newPhone !== this.profile.phone){
                data.phone = this.form.newPhone
            }
            if(this.role === 'client'){
                updateProfileData(data).then((res) => {
                    this.isLoading = false
                })
            } else {
                updateAdminProfileData(data).then((res) => {
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

.image-loader {
    margin-top: 16px;
}

label {
    font-size: 16px;
    color: #575757;
}

input {
    margin-top: 8px;
}

.no-image {
    width: 150px;
    height: 150px;
    background-color: #D9D9D9;
    border-radius: 75px;
    background-size: cover;
}

.img {
    width: 150px;
    height: 150px;
    border-radius: 75px;
    object-fit: cover;
    object-position: center;
}

.img-container {
    margin-top: 16px;
}

.name-surname {
    margin-top: 32px;
    display: flex;
    justify-content: space-between;
    width: 100%;
}

input[type="text"] {
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