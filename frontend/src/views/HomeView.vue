<script>
import TheNavbar from "@/components/TheNavbar.vue";
import {getAllCategories} from "@/services/adminServices.js";
import UploadProgress from "@/components/UploadProgress.vue";

export default{
    name: "HomeView",
    components: {UploadProgress, TheNavbar},
    data(){
        return {
            isLoading: false,
            categories: []
        }
    },
    beforeMount() {
        getAllCategories().then((res) => {
            if (res === "ERROR") {
                this.isLoading = false
            }
            else {
                this.isLoading = false
                this.categories = res
            }
        })
    },
    computed: {
        emptyCells() {
            const arr = []
            for(let i=this.categories.length; i<24; i++){
                arr.push(i)
            }
            return arr
        },
    },
    methods: {
        getCellClass(index) {
            const isTopRow = Math.floor(index / 8) === 0; // Проверка, верхняя ли строка
            const isFirstColumn = index % 8 === 0; // Проверка, первый ли столбец
            const isBottomRow = Math.floor(index / 8) === 2; // Проверка, последняя ли строка
            const isLastColumn = (index + 1) % 8 === 0; // Проверка, последний ли столбец
            return {
                'no-top-border': isTopRow,
                'no-left-border': isFirstColumn,
                'no-bottom-border': isBottomRow,
                'no-right-border': isLastColumn,
            };
        }
    }
}
</script>

<template>
    <UploadProgress v-if="isLoading"></UploadProgress>
    <TheNavbar></TheNavbar>
    <main>
        <div class="categories">
            <div class="header">
                Категории
            </div>
            <div class="table">
                <div class="grid">
                    <div
                        class="cell"
                        v-for="(category, index) in categories"
                        :key="index"
                        :class="getCellClass(index)"
                    >
                        <span>
                            {{ category.name }}
                        </span>

                    </div>
                    <div
                        class="cell"
                        v-for="index in emptyCells"
                        :key="{index}"
                        :class="getCellClass(index)"
                    ></div>
                </div>
            </div>

        </div>
    </main>
</template>

<style scoped>
main {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.categories{
    margin-top: 64px;
    width: 1184px;
    height: 440px;
}

.categories .header {
    position: relative;
    margin-bottom: -24px;
    width: 192px;
    height: 48px;
    background-color: #5FB955;
    border-radius: 2px;
    margin-left: 48px;
    font-size: 20px;
    font-weight: 600;
    padding-left: 40px;
    padding-top: 10px;
}

.table {
    width: 100%;
    height: 418px;
    border-radius: 10px;
    background-image:  url("../assets/img/tool-box.png");
    padding-top: 42px;
    padding-left: 48px;
    padding-right: 48px;
}

.grid {
    margin-top: 1px;
    display: grid;
    grid-template-columns: repeat(8, 1fr); /* 6 колонок */
}

.cell {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 112px;
    border: 1px solid rgba(0, 0, 0, 0.2);

}

.cell span {
    width: min-content;
}

.no-top-border {
    border-top: none;
}

.no-bottom-border {
    border-bottom: none;
}

.no-left-border {
    border-left: none;
}

.no-right-border {
    border-right: none;
}
</style>
