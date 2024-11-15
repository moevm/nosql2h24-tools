<template>
    <div v-if="show" class="modal">
        <div class="modal-content">
            <button @click="closeModal" class="close">
                <img src="../../assets/svg/close.svg" alt="close"/>
            </button>
            <p v-for="error in errors">{{ error }}</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ErrorModal',
    props: {
        show: {
            type: Boolean,
            required: true
        },
        errors: {
            type: Array,
            required: true
        }
    },
    methods: {
        closeModal() {
            this.$emit('close')
        }
    },
};
</script>

<style scoped>
/* Стили для модального окна */
.modal {
    display: block;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
    background-color: #DA686A;
    margin: 15% auto;
    padding: 32px 64px;
    border: 3px solid #760A0C;
    width: 50%;
    border-radius: 10px;
}

.close {
    display: inline;
    left: 70%;
    position: absolute;
}

.close:hover,
.close:focus {
    color: #000;
    text-decoration: none;
    cursor: pointer;
}

p:has(+ p) {
    margin-bottom: 16px;
}

p {
    font-size: 24px;
}
</style>