<script>
import AddNewCategory from "@/components/admin/AddNewCategory.vue";
import AddNewTool from "@/components/admin/AddNewTool.vue";
import {getAllCategories} from "@/services/adminServices.js";
import CategoriesTable from "@/components/tables/CategoriesTable.vue";
import AddNewType from "@/components/admin/AddNewType.vue";
import UploadProgress from "@/components/UploadProgress.vue";

export default {
    name: "AdminCategories",
    components: {UploadProgress, AddNewType, CategoriesTable, AddNewTool, AddNewCategory},
    data() {
        return {
            isLoading: false,
            categories: [],
            isNewCategoryPanelOpen: false,
            isNewTypePanelOpen: false,
        }
    },
    methods: {
        openNewCategoryPanel() {
            this.isNewTypePanelOpen = false
            this.isNewCategoryPanelOpen = true
        },
        openNewTypePanel(){
            this.isNewCategoryPanelOpen = false
            this.isNewTypePanelOpen = true
        },
        closeNewCategoryPanel() {
            this.isNewCategoryPanelOpen = false
        },
        closeNewTypePanel(){
            this.isNewTypePanelOpen = false
        },
    },
    beforeMount() {
        getAllCategories().then((res) => {
            if (res === "ERROR") window.location.href = '/'
            else {
                this.isLoading = false
                this.categories = res
            }
        })
    }
}
</script>

<template>
    <UploadProgress v-if="isLoading"></UploadProgress>
    <div class="main">
        <AddNewCategory :isOpen="isNewCategoryPanelOpen" @close=closeNewCategoryPanel />
        <AddNewType :isOpen="isNewTypePanelOpen" @close=closeNewTypePanel :categories="categories"/>
        <div class="header">
            <span class="title">Категории и типы</span>
        </div>
        <div class="content">
            <div class="actions">
                <button class="add-new-btn" @click=openNewCategoryPanel>+ Добавить новую категорию</button>
                <button class="add-new-btn" @click=openNewTypePanel>+ Добавить новый тип</button>
            </div>
            <CategoriesTable :categories="categories"/>
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

.content {
    padding-top: 32px;
    padding-bottom: 64px;
}

.title {
    font-size: 26px;
    font-weight: bold;
}

.add-new-btn {
    padding: 10px 16px;
    background-color: #A1DA68;
    border: 1px solid #575757;
    border-radius: 10px;
    font-weight: 600;
    margin-right: 32px;
}

.actions {
    margin-bottom: 32px;
}
</style>