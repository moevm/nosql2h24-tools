<template>
    <UploadProgress v-if="isLoading"></UploadProgress>
    <div class="content">
        <div class="header">
            <h1>Результаты поиска по запросу «{{ query }}»</h1>
        </div>
        <div class="mt-32">
            <div class="filters">
                <form @submit.prevent="handleSubmit" novalidate>
                    <div class="categories-header">
                        <h2>Категория</h2>
                        <span v-if="categoriesVisible" @click="categoriesVisible=false">Скрыть</span>
                        <span v-else @click="categoriesVisible=true">Показать</span>
                    </div>

                    <div v-for="(item, index) in categories" :key="index" class="categories" v-if="categoriesVisible">
                        <label>
                            <input
                                type="checkbox"
                                :value="item.name"
                                v-model="selectedCategories"
                            />
                            <span class="ml-16">
                           {{ item.name }}
                        </span>
                        </label>
                    </div>

                    <div class="categories-header mt-32">
                        <h2>Тип</h2>
                        <span v-if="typesVisible" @click="typesVisible=false">Скрыть</span>
                        <span v-else @click="typesVisible=true">Показать</span>
                    </div>

                    <div v-for="(item, index) in types" :key="index" class="categories" v-if="typesVisible">
                        <label>
                            <input
                                type="checkbox"
                                :value="item.name"
                                v-model="selectedTypes"
                            />
                            <span class="ml-16">
                           {{ item.name }}
                        </span>
                        </label>
                    </div>

                    <div class="categories-header mt-32">
                        <h2>Цена</h2>
                    </div>
                    <div class="categories price">
                        <input type="number" v-model="minPrice" min="0" step="1"/>
                        -
                        <input type="number" v-model="maxPrice" min="1" step="1"/>
                    </div>
                    <button type="submit">Применить фильтры</button>

                </form>

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
    </div>
</template>

<script>
import ToolCard from "@/components/tool/ToolCard.vue";
import UploadProgress from "@/components/UploadProgress.vue";
import {VueAwesomePaginate} from "vue-awesome-paginate";
import {getSearchTools} from "@/services/toolServices.js";
import {getAllCategories} from "@/services/adminServices.js";
import {useToast} from "vue-toastification";

export default {
    name: "ToolsSearch",
    components: {VueAwesomePaginate, UploadProgress, ToolCard},
    setup() {
        const toast = useToast();
        return {toast}
    },
    data() {
        return {
            isLoading: true,
            tools: {},
            toolsCount: 0,
            currentPage: 1,
            categories: [],
            selectedCategories: [],
            selectedTypes: [],
            categoriesVisible: true,
            typesVisible: true,
            minPrice: 0,
            maxPrice: 100000,
        }
    },
    computed: {
        query() {
            return this.$route.params.search
        },
        types() {
            const typesArr = []
            this.categories.map((cat) => {
                if(cat.types){
                     cat.types.map((type) => {
                         typesArr.push(type)
                     })
                 }
            })
            return typesArr
        }
    },
    watch: {
        '$route.params.search': {
            immediate: true,
            handler(newQuery) {
                this.fetchResults(newQuery);
            },
        }
    },
    mounted() {
        getAllCategories().then((data) => {
            this.categories = data
        })
        this.fetchResults(this.query);
    },
    methods:{
        fetchResults(newQuery) {
            this.selectedCategories = []
            this.selectedTypes = []
            this.maxPrice = 100000
            this.minPrice = 0
            getSearchTools(newQuery).then((data) => {
                this.tools["1"] = data.tools
                this.toolsCount = data.totalNumber
                this.isLoading = false
            })
        },

        fetchResultWithFilters(pageChange=false) {
            if(!pageChange){
                this.tools = {}
                this.currentPage = 1
            }
            const filters = {}
            filters.page = this.currentPage
            if(this.selectedTypes){
                filters.type = this.selectedTypes
            }
            if(this.selectedCategories){
                filters.category = this.selectedCategories
            }
            filters.page = this.currentPage
            filters.min_price = this.minPrice
            filters.max_price = this.maxPrice
            this.isLoading = true
            getSearchTools(this.query, filters).then((data) => {
                this.tools[this.currentPage] = data.tools
                this.toolsCount = data.totalNumber
                this.isLoading = false
            })
        },

        handleSubmit() {
            if(this.minPrice > this.maxPrice){
                this.toast.error("Минимальная цена должна быть меньше максимальной")
                return
            }
            this.currentPage = 1
            this.fetchResultWithFilters()
        },
        onPageChange() {
            if(this.tools[this.currentPage])
                return
            this.fetchResultWithFilters(true)
        }
    }
}
</script>

<style scoped>
.header {
    height: 100px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #D5D5D5;
}

h1 {
    font-size: 24px;
    font-weight: bold;
}

.content {
    padding-left: 32px;
    padding-right: 32px;
    padding-bottom: 64px;
}

.mt-32 {
    margin-top: 32px;
    display: flex;
    flex-direction: row;
}

.flex {
    margin-left: 64px;
    display: flex;
    flex-wrap: wrap;
    gap: 48px;
}

.filters {
    width: 250px;
}

.categories {
    width: 250px;
    margin-top: 16px;
}

.price {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

h2 {
    font-weight: 600;
    font-size: 18px;
}

label {
    display: flex;
    align-items: center;
    font-size: 16px;
}

.ml-16 {
    margin-left: 14px;
}

.categories-header {
    display: flex;
    justify-content: space-between;
}

input[type="checkbox"] {
    -webkit-appearance: none; /* Убираем стандартный вид */
    -moz-appearance: none;
    appearance: none;
    width: 20px; /* Задаем размер чекбокса */
    height: 20px;
    border: 2px solid #D1D1D1; /* Цвет рамки */
    border-radius: 4px; /* Скругление углов */
    outline: none;
    cursor: pointer;
    position: relative;
}

input[type="checkbox"]:checked {
    background-color: #6A983C; /* Цвет фона при активации чекбокса */
    border-color: #46760A; /* Изменяем цвет рамки при активации */
}

input[type="checkbox"]:checked::after {
    content: ''; /* Добавляем псевдоэлемент для галочки */
    position: absolute;
    top: 2px; /* Настройте положение галочки по вертикали */
    left: 6px; /* Настройте положение галочки по горизонтали */
    width: 6px;
    height: 12px;
    border: solid white; /* Цвет галочки */
    border-width: 0 2px 2px 0; /* Создаем галочку */
    transform: rotate(45deg); /* Поворачиваем */
}

input[type="number"] {
    width: 109px;
    height: 42px;
    border: 1px solid #D5D5D5;
    border-radius: 12px;
    padding: 8px;
}

form button {
    width: 240px;
    height: 40px;
    margin-top: 32px;
    padding: 8px;
    background-color: #6A983C;
    border-radius: 12px;
    border: 2px solid #46760A;
    color: #FFFFFF;
    font-weight: bold;
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



.paginator {
    margin-top: 32px;
    width: 100%;
    display: flex;
    justify-content: end;
}
</style>