<template>
    <div class="content">
        <table>
            <thead>
            <tr>
                <th>Имя</th>
                <th>Фамилия</th>
                <th>Телефон</th>
                <th>Электронная почта</th>
                <th>Должность</th>
                <th>Дата присоединения</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(worker, index) in workers" :key="index">
                <td>{{ worker.name }}</td>
                <td>{{ worker.surname }}</td>
                <td>{{ worker.phone }}</td>
                <td>{{ worker.email}}</td>
                <td>{{ worker.jobTitle }}</td>
                <td>{{ getDate(worker.date) }}</td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    name: 'EmployeesTable',
    props: {
        workers: {
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