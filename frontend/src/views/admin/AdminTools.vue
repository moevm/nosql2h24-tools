<script>
import ToolCard from "@/components/tool/ToolCard.vue";
import {getAllCategories, getTools, getToolsPagesCount} from "@/services/adminServices.js";
import {VueAwesomePaginate} from "vue-awesome-paginate";
import UploadProgress from "@/components/UploadProgress.vue";
import AddNewTool from "@/components/admin/AddNewTool.vue";

export default {
    name: "AdminTools",
    components: {AddNewTool, UploadProgress, VueAwesomePaginate, ToolCard},
    data() {
        return {
            categories: [],
            categoriesWithTypes: [],
            isNewToolPanelOpen: false,
            isLoading: false,
            tools: {},
            toolsCount: 0,
            currentPage: 1,
        }
    },
    methods: {
        onPageChange() {
            if (this.tools[this.currentPage])
                return
            this.isLoading = true
            getTools(this.currentPage).then((res) => {
                this.isLoading = false
                if (res === "ERROR") window.location.href = '/'
                this.tools[this.currentPage] = res;
            });
        }
    },
    beforeMount() {
        getTools().then((res) => {
            if (res === "ERROR") window.location.href = '/'
            this.tools["1"] = res;
        });
        getToolsPagesCount().then((res) => {
            if (res === "ERROR") window.location.href = '/'
            this.toolsCount = res.pages
        });
        getAllCategories().then((res) => {
            if (res === "ERROR") window.location.href = '/'
            else {
                this.isLoading = false
                this.categories = res
                this.categories.forEach((cat) => {
                    if(cat.types.length > 0) this.categoriesWithTypes.push(cat)
                })
            }
        })
    }
}
</script>

<template>
    <div class="main">
        <AddNewTool :isOpen="isNewToolPanelOpen" @close="isNewToolPanelOpen = false" :categories="categoriesWithTypes" />
        <div class="header">
            <span class="title">Инструменты</span>
        </div>
        <div class="content" >
            <div class="actions">
                <button class="add-new-btn" @click="isNewToolPanelOpen=true">+ Добавить новый инструмент</button>
            </div>

            <div class="load">
                <UploadProgress v-if="isLoading"></UploadProgress>
            </div>

            <div class="flex">
                <div v-for="tool in tools[currentPage]">
                    <ToolCard
                        :image="tool.images[0]"
                        :title="tool.name"
                        :description="tool.description"
                        :rating="tool.rating"
                        :dailyPrice="tool.dailyPrice"
                        :id=tool._id
                    />
                </div>
            </div>
            <div class="paginator">
                <vue-awesome-paginate
                    :total-items="toolsCount"
                    :items-per-page="12"
                    :max-pages-shown="5"
                    v-model="currentPage"
                    paginate-buttons-class="btn"
                    active-page-class="btn-active"
                    back-button-class="back-btn"
                    next-button-class="next-btn"
                    @click="onPageChange"
                />
            </div>

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

.content {
    padding-top: 32px;
    padding-bottom: 64px;
}

.flex {
    display: flex;
    flex-wrap: wrap;
    gap: 48px;
}

.inline-block {
    display: inline-block;
}

.load {
    position: relative;
    width: 100%;
    height: 100%;
}

>>> .btn {
    height: 30px;
    width: 30px;
    border: none;
    margin: 4px;
    cursor: pointer;
    border-radius: 3px;
    font-weight: bold;
    background-color: #D9D9D9;
}

>>> .back-btn {
    background-color: #D9D9D9;
}

>>> .next-btn {
    background-color: #D9D9D9;
}

>>> .btn-active {
    background-color: #6A983C;
    color: white;
}

.add-new-btn {
    padding: 10px 16px;
    background-color: #A1DA68;
    border: 1px solid #575757;
    border-radius: 10px;
    font-weight: 600;
}

.actions {
    margin-bottom: 32px;
}

.paginator {
    margin-top: 32px;
    width: 100%;
    display: flex;
    justify-content: end;
}
</style>