<script>
export default {
    name: "ToolCard",
    props: {
        image: {
            type: String,
            default: "",
            required: false,
        },
        id: {
            type: String,
            required: true,
        },
        title: {
            type: String,
            required: true,
        },
        description: {
            type: String,
            required: true,
        },
        rating: {
            type: Number,
            required: true,
        },
        dailyPrice: {
            type: Number,
            required: true
        }
    },
    methods: {
        range(num) {
            return Array.from({ length: num }, (v, k) => k)
        },
    }
}
</script>

<template>
    <div class="card">
        <template v-if="image">
            <figure>
                <img :src="image" alt="image">
            </figure>
        </template>
        <template v-else>
            <div class="no-image"></div>
        </template>
        <span class="title">{{title}}</span>
        <span class="description" v-if="description">{{description}}</span>
        <div class="stars">
            <template v-for="i in range(rating)">
                <img src="../../assets/svg/stars/black_star.svg" alt="star" />
            </template>
            <template v-for="i in range(5 - rating)">
                <img src="../../assets/svg/stars/star.svg" alt="star" />
            </template>
        </div>
        <span class="price">{{dailyPrice}}₽</span>
        <button class="rent">Арендовать</button>
    </div>
</template>

<style scoped>
.card {
    width: 250px;
    height: 410px;
    padding: 18px;
    border: 1px solid #D1D1D1;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
}

figure {
    border-radius: 12px;
    width: 100%;
    height: 180px;
    overflow: hidden;
}

img {
    width: 100%;
}

.no-image {
    width: 100%;
    height: 180px;
    background-color: #F9F9F9;
}

.title {
    margin-top: 16px;
    font-weight: 500;
    font-size: 15px;
}

.description {
    margin-top: 4px;
    font-size: 12px;
    font-weight: 400;
    color: #575757;
}

.stars {
    margin-top: 32px;
    width: 100%;
    height: 16px;
    display: flex;
    flex-direction: row;
}

.stars img {
    width: 16px;
    height: 16px;
    margin-right: 2px;
}

.price {
    margin-top: 16px;
    font-weight: 600;
    font-size: 18px;
}

.rent {
    margin-top: 16px;
    background-color: #6A983C;
    width: 100%;
    height: 36px;
    font-size: 15px;
    font-weight: bold;
    color: #FFFFFF;
    border: 2px solid #46760A;
    border-radius: 12px;
}

.pagination-container {
    display: flex;

    column-gap: 10px;
}

.paginate-buttons {
    height: 40px;

    width: 40px;

    border-radius: 20px;

    cursor: pointer;

    background-color: rgb(242, 242, 242);

    border: 1px solid rgb(217, 217, 217);

    color: black;
}

.paginate-buttons:hover {
    background-color: #d8d8d8;
}

.active-page {
    background-color: #3498db;

    border: 1px solid #3498db;

    color: white;
}

.active-page:hover {
    background-color: #2988c8;
}
</style>