<template>
    <div class="content">
        <table>
            <thead>
            <tr>
                <th>ID</th>
                <th>Заказчик</th>
                <th>Цена</th>
                <th>Сроки аренды</th>
                <th>Инструменты</th>
                <th>Способ получения</th>
                <th>Способ оплаты</th>
                <th>Создано</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="order in orders" :key="order._id">
                <td style="word-wrap: break-word; max-width: 100px;">{{ order._id }}</td>
                <td>{{ order.client.surname}} {{order.client.name}}</td>
                <td>{{ order.price }}</td>
                <td>{{ getDate(order.start_leasing) }} - {{getDate(order.end_leasing)}}</td>
                <td>{{ getToolsNames(order.tools) }}</td>
                <td>{{ getGetting(order.delivery_type) }}</td>
                <td>{{ getPayment(order.payment_type) }}</td>
                <td>{{ getDate(order.create_order_time) }}</td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    name: 'OrdersWorkerTable',
    props: {
        orders: {
            required: true,
            type: Array
        }
    },
    mounted() {
    },
    methods: {
        getToolsNames(tools) {
            let names = ""
            tools.map((tool) => {
                names += tool.name + '\n'
            })
            return names
        },
        getDate(isoString) {
            const date = new Date(isoString);
            const options = {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
            };
            return date.toLocaleString('ru-RU', options);
        },
        getPayment(method) {
            if(method === "card") return "Банковской картой"
            else return "Наличными"
        },
        getGetting(method) {
            if(method === "to_door") return "Доставка"
            else return "Самовывоз"
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
</style>