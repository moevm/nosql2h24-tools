<template>
    <div class="main">
        <div class="header">
            <span class="title">Сотрудники</span>
        </div>
        <div class="content">
            <div class="filters">
                <label>
                    Фильтр по имени <br />
                    <input type="text" v-model="name" placeholder="Имя"/>
                </label>
                <label>
                    Фильтр по фамилии <br/>
                    <input type="text" v-model="surname" placeholder="Фамилия"/>
                </label>
                <label>
                    Фильтр по телефону <br/>
                    <input type="text" v-model="phone" placeholder="Телефон"/>
                </label>
                <label>
                    Фильтр по электронной почте <br/>
                    <input type="text" v-model="email" placeholder="Электронная почта"/>
                </label>
                <label>
                    Фильтр по должности <br/>
                    <input type="text" v-model="jobTitle" placeholder="Должность"/>
                </label>
            </div>
            <button class="handle-filters" @click="handleFilters">
                Применить фильтры
            </button>
            <EmployeesTable :workers="workers[currentPage]" class="mt-32"/>
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
import ToolCart from "@/components/tool/ToolCard.vue";
import OrdersTable from "@/components/tables/OrdersTable.vue";
import EmployeesTable from "@/components/tables/EmployeesTable.vue";
import {getWorkers} from "@/services/workerServices.js";
import {VueAwesomePaginate} from "vue-awesome-paginate";

export default {
    name: "AdminEmployees",
    components: {VueAwesomePaginate, EmployeesTable, OrdersTable, ToolCart},
    data() {
        return {
            workers: {},
            name: "",
            surname: "",
            jobTitle: "",
            email: "",
            phone: "",
            currentPage: 1,
            totalNumber: 0
        }
    },
    beforeMount() {
        getWorkers().then((data) => {
            this.workers[this.currentPage] = data.workers
            this.totalNumber = data.totalNumber
        })
    },
    methods: {
        handleFilters(){
            const filters = {}
            if(this.name) {
                filters.name = this.name
            }
            if(this.surname) {
                filters.surname = this.surname
            }
            if(this.jobTitle) {
                filters.jobTitle = this.jobTitle
            }
            if(this.email) {
                filters.email =this.email
            }
            if(this.phone) {
                filters.phone = this.phone
            }
            getWorkers(filters).then((data) => {
                this.workers[this.currentPage] = data.workers
                this.totalNumber = data.totalNumber
            })
        },
        onPageChange() {

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
    margin-top: 64px;
}

.filters {
    margin-top: 32px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 32px;
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