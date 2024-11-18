<template>
    <div class="content">
        <h1>Инструменты</h1>
        <table>
            <thead>
            <tr>
                <th>ID</th>
                <th>Цена</th>
                <th>Рейтинг</th>
                <th>Категория</th>
                <th>Тип</th>
                <th>Условие</th>
                <th>Создано</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="tool in tools" :key="tool._id">
                <td>{{ tool._id }}</td>
                <td>{{ tool.dailyPrice }}</td>
                <td>{{ tool.rating }}</td>
                <td>{{ tool.category }}</td>
                <td>{{ tool.type }}</td>
                <td>{{ tool.condition }}</td>
                <td>{{ tool.data }}</td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
//import axios from 'axios';

export default {
    name: 'OrdersTable',
    data() {
        return {
            tools: [],
        };
    },
    mounted() {
        this.fetchTools();
    },
    methods: {
        // async fetchTools() {
        //     try {
        //         const response = await axios.get('https://your-api-url.com/tools'); // Замените на ваш URL
        //         this.tools = response.data;
        //     } catch (error) {
        //         console.error('Ошибка при получении данных:', error);
        //     }
        // },
        fetchTools() {
            this.tools = [
                {'_id': '1111', 'dailyPrice': '2222', 'rating': '10', 'category': 'Ромашка', 'type': 'Gfgggfg', 'condition': 'Rsfdesf', 'data': '11.20.2024'},
                {'_id': '1111', 'dailyPrice': '2222', 'rating': '10', 'category': 'Ромашка', 'type': 'Gfgggfg', 'condition': 'Rsfdesf', 'data': '11.20.2024'},
                {'_id': '1111', 'dailyPrice': '2222', 'rating': '10', 'category': 'Ромашка', 'type': 'Gfgggfg', 'condition': 'Rsfdesf', 'data': '11.20.2024'},
                {'_id': '1111', 'dailyPrice': '2222', 'rating': '10', 'category': 'Ромашка', 'type': 'Gfgggfg', 'condition': 'Rsfdesf', 'data': '11.20.2024'},
                {'_id': '1111', 'dailyPrice': '2222', 'rating': '10', 'category': 'Ромашка', 'type': 'Gfgggfg', 'condition': 'Rsfdesf', 'data': '11.20.2024'},
                {'_id': '1111', 'dailyPrice': '2222', 'rating': '10', 'category': 'Ромашка', 'type': 'Gfgggfg', 'condition': 'Rsfdesf', 'data': '11.20.2024'},
                {'_id': '1111', 'dailyPrice': '2222', 'rating': '10', 'category': 'Ромашка', 'type': 'Gfgggfg', 'condition': 'Rsfdesf', 'data': '11.20.2024'},
                {'_id': '1111', 'dailyPrice': '2222', 'rating': '10', 'category': 'Ромашка', 'type': 'Gfgggfg', 'condition': 'Rsfdesf', 'data': '11.20.2024'},
                {'_id': '1111', 'dailyPrice': '2222', 'rating': '10', 'category': 'Ромашка', 'type': 'Gfgggfg', 'condition': 'Rsfdesf', 'data': '11.20.2024'},
                {'_id': '1111', 'dailyPrice': '2222', 'rating': '10', 'category': 'Ромашка', 'type': 'Gfgggfg', 'condition': 'Rsfdesf', 'data': '11.20.2024'},
                {'_id': '1111', 'dailyPrice': '2222', 'rating': '10', 'category': 'Ромашка', 'type': 'Gfgggfg', 'condition': 'Rsfdesf', 'data': '11.20.2024'},
            ]
        }
    },
};
</script>

<style scoped>
table {
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
    padding: 64px;
}
</style>