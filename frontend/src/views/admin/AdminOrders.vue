<template>
    <UploadProgress v-if="isLoading"></UploadProgress>
    <div class="main">
        <div class="header">
            <span class="title">Заказы</span>
        </div>
        <div class="content">
            <div class="filters">
                <label>
                    Фильтр по названию инструментов <br />
                    <input type="text" v-model="filterByToolName" placeholder="Название инструмента"/>
                </label>
                <label class="price-block">
                    Минимальная цена заказа <br/>
                    <input type="number" v-model="minPrice" min="0"/>
                </label>
                <label>
                    Максимальная цена заказа <br/>
                    <input type="number" v-model="maxPrice" min="0"/>
                </label>
                <label>
                    Минимальная дата заказа <br/>
                    <input type="date" v-model="startDate" @input="validateStartDate" :min="minDate"/>
                </label>
                <label>
                    Максимальная дата заказа <br/>
                    <input type="date" v-model="endDate" @input="validateEndDate"  :min="minEndDate"/>
                </label>
                <label>
                    Фильтр по имени заказчика <br />
                    <input type="text" v-model="name" placeholder="Имя заказчика"/>
                </label>
                <label>
                    Фильтр по фамилии заказчика <br />
                    <input type="text" v-model="surname" placeholder="Фамилия заказчика"/>
                </label>
            </div>
            <button class="handle-filters" @click="handleFilters">
                Применить фильтры
            </button>
            <OrdersWorkerTable :orders="orders[currentPage]" class="mt-64"/>
            <div class="paginator">
                <vue-awesome-paginate
                    :total-items="ordersNumber"
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
import {getAllOrders} from "@/services/orderServices.js";
import OrdersWorkerTable from "@/components/tables/OrdersWorkerTable.vue";
import UploadProgress from "@/components/UploadProgress.vue";
import {useToast} from "vue-toastification";
import {VueAwesomePaginate} from "vue-awesome-paginate";

export default {
    name: "AdminOrders",
    components: {VueAwesomePaginate, UploadProgress, OrdersWorkerTable},
    setup() {
        const toast = useToast()
        return {toast}
    },
    data() {
        return {
            isLoading: true,
            orders: {},
            filterByToolName: "",
            minPrice: 0,
            maxPrice: 0,
            startDate: "",
            endDate: "",
            dateError: "",
            name: "",
            surname: "",
            currentPage: 1,
            ordersNumber: 0
        }
    },
    computed: {
        minEndDate() {
            if (this.startDate) {
                const start = new Date(this.startDate);
                start.setDate(start.getDate() + 1);
                return start.toISOString().split('T')[0];
            }
        },
    },
    beforeMount() {
        getAllOrders().then((data) => {
            this.orders[this.currentPage] = data.orders
            this.ordersNumber = data.totalNumber
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
            if(this.minPrice && this.maxPrice){
                if(this.minPrice > this.maxPrice){
                    errors += "Максимальная сумма не должна быть меньше минимальной\n"
                }
            }
            return errors
        },
        getFilters() {
            const filters = []
            if(this.filterByToolName){
                filters.tool_name = [this.filterByToolName]
            }
            if(this.startDate){
                filters.start_date = this.startDate
            }
            if(this.endDate){
                filters.end_date = this.endDate
            }
            if(this.minPrice){
                filters.min_price = this.minPrice
            }
            if(this.maxPrice){
                filters.max_price = this.maxPrice
            }
            if(this.name) {
                filters.customer_name = this.name
            }
            if(this.surname) {
                filters.customer_surname = this.surname
            }
            filters.page = this.currentPage
            return filters
        },
        handleFilters() {
            const errors = this.validate()
            if(errors){
                this.toast.error(errors)
                return
            }
            const filters = this.getFilters()
            this.isLoading = true
            this.currentPage = 1
            getAllOrders(filters).then((data) => {
                this.orders[this.currentPage] = data.orders
                this.isLoading = false
            })
        },
        onPageChange(){
            if(this.orders[this.currentPage])
                return
            const filters = this.getFilters()
            this.isLoading = true
            getAllOrders(filters).then((data) => {
                this.orders[this.currentPage] = data.orders
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

.mt-64 {
    margin-top: 64px;
}

.filters {
    display: flex;
    flex-wrap: wrap;
    gap: 32px;
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

.handle-filters {
    background-color: #6A983C;
    border: 2px solid #46760A;
    color: #FFFFFF;
    font-weight: bold;
    padding: 8px 16px;
    border-radius: 12px;
    margin-top: 32px;
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