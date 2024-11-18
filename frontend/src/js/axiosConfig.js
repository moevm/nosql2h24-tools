import axios from 'axios';
import {getAccessToken, logoutUser, refreshToken} from "@/services/authService.js";

// Устанавливаем интерцептор для автоматической установки заголовка
axios.interceptors.request.use(
  async (config) => {
    const token = getAccessToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Интерцептор ответа для обновления токена при 401 ошибке
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const newToken = await refreshToken();
        axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
        originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
        return axios(originalRequest);
      } catch (error) {
        logoutUser();
        window.location.href = '/';
      }
    }
    return Promise.reject(error);
  }
);