<script>
import ToolCart from "@/components/tool/ToolCard.vue";

export default {
    name: "AdminEmployees",
    components: {ToolCart},
    data() {
      return {
          employees: []
      }
    },
    beforeMount() {

    }
}
</script>

<template>
    <div class="main">
        <div class="header">
            <span class="title">Сотрудники</span>
        </div>
        <div class="content">

        </div>
    </div>
</template>

<style scoped>
.main {
    padding: 0 64px;
}

.header {
    height: 96px;
    width: 100%;
    display: flex;
    align-items: center;
    border-bottom: 1px solid rgba(0, 0, 0, 0.20);
}

.title {
    font-size: 26px;
    font-weight: bold;
}
</style>