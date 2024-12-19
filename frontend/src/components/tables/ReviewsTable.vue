<template>
    <div class="content">
        <table>
            <thead>
            <tr>
                <th>Имя</th>
                <th>Фамилия</th>
                <th>Оценка</th>
                <th>Инструмент</th>
                <th>Текст</th>
                <th>Дата</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(review, index) in reviews" :key="index">
                <td>{{ review.reviewer_name }}</td>
                <td>{{ review.reviewer_surname }}</td>
                <td>
                    <template v-for="i in range(review.rating)">
                        <img src="../../assets/svg/stars/black_star.svg" alt="star" />
                    </template>
                    <template v-for="i in range(5 - review.rating)">
                        <img src="../../assets/svg/stars/star.svg" alt="star" />
                    </template>
                </td>
                <td>{{ review.tool_name}}</td>
                <td>{{ review.text }}</td>
                <td>{{ getDate(review.date) }}</td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    name: 'ReviewsTable',
    props: {
        reviews: {
            required: true,
            type: Array
        }
    },
    methods: {
        getDate(isoString) {
            const date = new Date(isoString);
            const options = {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
            };
            return date.toLocaleString('ru-RU', options);
        },
        range(num) {
            return Array.from({ length: num }, (v, k) => k)
        },
    },
};
</script>

<style scoped>
table {
    width: 100%;
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

.id {
    cursor: pointer;
    color: #6A983C;
}
</style>