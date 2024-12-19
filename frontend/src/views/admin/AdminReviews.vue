<template>
    <UploadProgress v-if="isLoading" />
    <div class="main">
        <div class="header">
            <span class="title">Отзывы</span>
        </div>
        <div class="content">
            <div class="filters">
                <label>
                    Фильтр по названию инструмента <br />
                    <input type="text" v-model="toolName" placeholder="Название инструмента"/>
                </label>
                <label>
                    Фильтр по имени отзывчика <br />
                    <input type="text" v-model="reviewerName" placeholder="Имя отзывчика"/>
                </label>
                <label>
                    Фильтр по фамилии отзывчика <br />
                    <input type="text" v-model="reviewerSurname" placeholder="Фамилия отзывчика"/>
                </label>
                <label>
                    Фильтр по оценке <br />
                    <input type="number" v-model="rating" min="0" max="5"/>
                </label>
                <label>
                    Минимальная дата <br/>
                    <input type="date" v-model="startDate" @input="validateStartDate" :min="minDate"/>
                </label>
                <label>
                    Максимальная дата <br/>
                    <input type="date" v-model="endDate" @input="validateEndDate"  :min="minEndDate"/>
                </label>
            </div>
            <button class="handle-filters" @click="handleFilters">
                Применить фильтры
            </button>
            <ReviewsTable :reviews="reviews[currentPage]" class="mt-32" />
            <div class="paginator">
                <vue-awesome-paginate
                    :total-items="totalNumber"
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

<script>
import ReviewsTable from "@/components/tables/ReviewsTable.vue";
import {getAllReviews} from "@/services/reviewServices.js";
import UploadProgress from "@/components/UploadProgress.vue";
import {VueAwesomePaginate} from "vue-awesome-paginate";

export default {
    name: "AdminReviews",
    components: {VueAwesomePaginate, UploadProgress, ReviewsTable},
    data() {
        return {
            isLoading: true,
            reviews: {},
            currentPage: 1,
            totalNumber: 0,
            toolName: "",
            reviewerName: "",
            reviewerSurname: "",
            rating: 0,
            startDate: "",
            endDate: "",
            dateError: false
        }
    },
    beforeMount() {
        getAllReviews().then((data) => {
            this.reviews[this.currentPage] = data.reviews
            this.totalNumber = data.totalNumber
            this.isLoading = false
        })
    },
    methods: {
        validateStartDate() {
            this.dateError = this.startDate && this.endDate && new Date(this.startDate) >= new Date(this.endDate);
        },
        validateEndDate() {
            this.dateError = this.startDate && this.endDate && new Date(this.startDate) >= new Date(this.endDate);
        },
        validate() {
            let errors = ""
            if(this.dateError){
                errors += "Конечная дата должна быть как минимум на 1 день позже начальной даты.\n"
            }
            if(this.rating > 5 || this.rating < 0){
                errors += "Оценка должна быть в диапазоне от 0 до 5"
            }
            return errors
        },
        onPageChange() {
            if (this.reviews[this.currentPage]){
                return
            }
            const filters = this.getFilters()
            this.isLoading = true
            getAllReviews(filters).then((data) => {
                this.reviews[this.currentPage] = data.reviews
                this.isLoading = false
            })
        },
        getFilters() {
            const filters = []
            if (this.toolName){
                filters.tool_name = this.toolName
            }
            if (this.reviewerName){
                filters.reviewer_name = this.reviewerName
            }
            if (this.reviewer_surname){
                filters.reviewer_surname = this.reviewerSurname
            }
            if (this.rating){
                filters.rating = this.rating
            }
            if (this.startDate){
                filters.start_date = this.startDate
            }
            if (this.endDate){
                filters.end_date = this.endDate
            }
            filters.page = this.currentPage
            return filters
        },
        handleFilters() {
            const filters = this.getFilters()
            this.isLoading = true
            getAllReviews(filters).then((data) => {
                this.currentPage = 1
                this.reviews[this.currentPage] = data.reviews
                this.totalNumber = data.totalNumber
                this.isLoading = false
            })
        }
    }
}
</script>

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

.mt-32 {
    margin-top: 32px;
}

.filters {
    display: flex;
    flex-wrap: wrap;
    gap: 32px;
    margin-top: 32px;
}

.handle-filters {
    background-color: #6A983C;
    border: 2px solid #46760A;
    color: #FFFFFF;
    font-weight: bold;
    padding: 8px 16px;
    border-radius: 12px;
    margin-top: 32px;
}


input {
    height: 42px;
    background-color: #F9F9F9;
    border-radius: 12px;
    border: 1px solid #D1D1D1;
    padding-left: 16px;
    padding-right: 16px;
    margin-top: 8px;
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