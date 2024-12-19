<template>
    <div>
        <button @click="toggleSidebar" class="toggle-button">
            <img src="../assets/svg/sidebar/right.svg" alt="no" class="sidebar-button" :class="isOpen ? 'close-sidebar' : 'open-sidebar'"/>
        </button>

        <div class="sidebar" :style="{ transform: isOpen ? 'translateX(0)' : 'translateX(-100%)'}">
            <div class="import-section">
                <label for="jsonImport" class="import-label">Загрузить файл</label>
                <input
                    type="file"
                    id="jsonImport"
                    @change="handleFileUpload"
                    accept="application/json"
                    class="import-input"
                />
                <p v-if="!uploadedJsonData" class="import-text">Выберите JSON файл для импорта</p>
                <p v-else class="import-text">Файл успешно загружен</p>
            </div>
            <button @click="handleImport" class="export-button">
                Import
            </button>

            <button @click="handleExport" class="export-button">
                Export
            </button>

            <!-- Навигационные ссылки -->
            <div class="link" :class="{ active: isActive('/admin/dashboard') }">
                <router-link to="/admin/dashboard">
                    <p>Информационная<br>панель</p>
                </router-link>
            </div>
            <div class="link" :class="{ active: isActive('/admin/tools') }">
                <router-link to="/admin/tools">
                    <p>Инструменты</p>
                </router-link>
            </div>
            <div class="link" :class="{ active: isActive('/admin/categories') }">
                <router-link to="/admin/categories">
                    <p>Категории и типы</p>
                </router-link>
            </div>
            <div class="link" :class="{ active: isActive('/admin/employees') }">
                <router-link to="/admin/employees">
                    <p>Сотрудники</p>
                </router-link>
            </div>
            <div class="link" :class="{ active: isActive('/admin/orders') }">
                <router-link to="/admin/orders">
                    <p>Заказы</p>
                </router-link>
            </div>
            <div class="link" :class="{ active: isActive('/admin/reviews') }">
                <router-link to="/admin/reviews">
                    <p>Отзывы</p>
                </router-link>
            </div>
            <div class="link" :class="{ active: isActive('/admin/statistics') }">
                <router-link to="/admin/statistics">
                    <p>Статистика</p>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
import {exportData, importData} from "@/services/importExport.js";

export default {
    name: 'AdminSideBar',
    data() {
        return {
            isOpen: false,
            isCatalogue: false,
            uploadedJsonData: null,
            downloadedJsonData: null,
        };
    },
    methods: {
        toggleSidebar() {
            this.isOpen = !this.isOpen;
        },
        isActive(route) {
            return this.$route.path === route;
        },
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const jsonData = JSON.parse(e.target.result);
                    this.uploadedJsonData = jsonData;
                } catch (err) {
                    console.error('Некорректный JSON файл', err);
                }
            };
            reader.readAsText(file);
        },
        handleImport() {
            if(!this.uploadedJsonData){
                this.toast.error("Загрузите JSON файл!")
                return
            }
            importData(this.uploadedJsonData)
        },
        async handleExport() {
            try {
                exportData().then((data) => {
                    this.downloadedJsonData = data
                    this.downloadJsonFile(this.downloadedJsonData, 'exported_data.json');
                })
            } catch (error) {
                this.toast.error('Ошибка при экспорте данных:', error);
            }
        },
        downloadJsonFile(data, filename) {
            const jsonStr = JSON.stringify(data, null, 2);
            const blob = new Blob([jsonStr], { type: 'application/json' });
            const url = URL.createObjectURL(blob);

            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            document.body.appendChild(link);
            link.click();

            URL.revokeObjectURL(url);
            document.body.removeChild(link);
        },
    }
};
</script>

<style scoped>
.sidebar {
    z-index: 5000;
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 250px; /* Ширина боковой панели */
    background-color: #FFFFFF;
    color: black; /* Изменил цвет текста на черный для лучшей читаемости */
    padding: 10px;
    box-shadow: 2px 0 5px rgba(0,0,0,0.5);
    transition: transform 0.5s;
}
.toggle-button {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 10000;
}
.close-button {
    color: black;
    margin-top: 20px;
}

.open-sidebar {
    position: fixed;
    top: 50%;
    transform: translateX(-25%);
    width: 64px;
    height: 64px;
}

.close-sidebar {
    position: fixed;
    top: 50%;
    transform: translateX(310%) rotate(180deg);
    width: 64px;
    height: 64px;
}

.sidebar-button {
    transition: transform 0.5s;
}

.link {
    border-left: 3px solid rgba(0, 0, 0, 0.2);
    padding: 8px 16px;
    margin-top: 10px;
}

.link p {
    color: black;
}

.link.active {
    border-left: 3px solid #6A983C;
}

.import-section {
    margin-bottom: 20px;
}

.import-input {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0,0,0,0);
    white-space: nowrap;
    border: 0;
    padding: 0;
    margin: -1px;
}

.import-label {
    display: inline-block;
    background-color: #6A983C;
    color: #ffffff;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s;
    margin-bottom: 5px;
}

.import-label:hover {
    background-color: #5a7f2c;
}

.import-text {
    font-size: 14px;
    color: #333;
    margin: 0;
}

.export-button {
    display: block;
    width: 100%;
    padding: 8px 16px;
    margin-bottom: 20px;
    background-color: #6A983C;
    color: white;
    font-weight: bold;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
    border: 2px solid #46760A;
}

.export-button:hover {
    background-color: #46760A;
}

input[type="file"]{
    width: 300px;
}
</style>