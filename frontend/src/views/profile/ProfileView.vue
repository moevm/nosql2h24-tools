<template>
    <UploadProgress v-if="isLoading"  />
    <main>
        <ProfileSideBar :role="role"/>
        <div class="content">
            <div class="img-container" :style="backgroundImageStyle"></div>
            <div class="name-email">
                <p class="name">
                    {{profile.surname}} {{profile.name}}
                </p>
                <p class="email">
                    {{profile.email}}
                </p>
            </div>
            <div class="ml-32">
                <p v-if="profile.jobTitle" class="phone">
                    Должность: {{profile.jobTitle}}
                </p>
                <p v-if="profile.phone" class="phone">
                    Контакты: {{profile.phone}}
                </p>
            </div>
        </div>
    </main>

</template>

<script>
import ProfileSideBar from "@/components/ProfileSideBar.vue";
import {getProfileData} from "@/services/profileServices.js";
import UploadProgress from "@/components/UploadProgress.vue";
import {getAdminProfileData} from "@/services/adminProfileServices.js";

export default {
    name: "ProfileView",
    components: {UploadProgress, ProfileSideBar},
    data(){
        return {
            isLoading: true,
            profile: {}
        }
    },
    props: ['role'],
    beforeMount() {
        if(this.role === 'client'){
            getProfileData().then((data) => {
                this.profile = data
                this.isLoading = false
            })
        }
        else {
            getAdminProfileData().then((data) => {
                this.profile = data
                this.isLoading = false
            })
        }

    },
    computed: {
        backgroundImageStyle() {
            return this.profile.image
                ? { backgroundImage: `url(${this.profile.image})` }
                : {};
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
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 32px 64px;
}

.img-container {
    width: 150px;
    height: 150px;
    background-color: #D9D9D9;
    border-radius: 75px;
    background-size: cover;
}

.name-email{
    margin-left: 36px;
}

.name {
    font-size: 32px;
    font-weight: 600;
}

.email {
    font-size: 20px;
    font-weight: 600;
}

.ml-32 {
    margin-left: 64px;
}

.phone {
    font-weight: 500;
    font-size: 18px;
}
</style>