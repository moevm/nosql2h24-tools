<template>
    <main>
        <ProfileSideBar />
    </main>
</template>

<script>
import ProfileSideBar from "@/components/ProfileSideBar.vue";

export default {
    name: "MyRents",
    components: {ProfileSideBar}
}
</script>

<style scoped>
main {
    padding: 32px 64px;
}
</style>