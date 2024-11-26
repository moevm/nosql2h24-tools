<template>
    <div class="content">
        <table class="main-table">
            <thead>
            <tr>
                <th>Название</th>
                <th>Типы</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="category in categories" >
                <td>{{ category.name }}</td>
                <td>
                    <table>
                        <tr v-for="type in category.types">
                            <td>
                                {{type.name}}
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
//import axios from 'axios';

export default {
    name: 'CategoriesTable',
    props: {
        categories: {
            type: Array,
            default: false,
        },
    },
};
</script>

<style scoped>
.main-table {
    width: 1152px;
    border-collapse: collapse;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
}

th {
    background-color: #A1DA68;
}

.content {
    width: 100%;
}
</style>