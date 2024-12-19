import axios from 'axios';
import {jwtDecode} from "jwt-decode";
import store from "@/js/store.js";
import { useToast } from 'vue-toastification'

const toast = useToast()

const API_URL = 'http://localhost:8000/api/auth';

export const register = async (userData) => {
  try{
    const response = await axios.post(`${API_URL}/register/client`, userData, {
      headers: {
        'Content-Type': 'application/json'
      }  });
    toast.success("Регистрация прошла успешно!\n Пожалуйста, войдите в свой аккаунт.")
    return "SUCCESS"
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage)
    return "ERROR"
  }
};

export const login = async (userData) => {
  try{
    const response = await axios.post(`${API_URL}/token`, userData, {
      headers: {
        'Content-Type': 'application/json'
      }  });
    toast.success("Авторизация прошла успешно!")
    storeUserInfo(response.data.access_token)
    return "SUCCESS"
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage)
    return "ERROR"
  }
};

export const storeUserInfo = (token) => {
  storeAccessToken(token);
  const decodedToken = jwtDecode(token);
  const isAdmin = (decodedToken.role === "worker") || false;
  const isAuthenticated = true;
  const id = decodedToken.sub

  localStorage.setItem('isAdmin', isAdmin.toString());
  localStorage.setItem('id', id);
  localStorage.setItem('isAuthenticated', isAuthenticated.toString());
  store.commit('login')
}

export const isUserAdmin = () => {
  return localStorage.getItem('isAdmin') === 'true';
};

export const isUserAuthenticated = () => {
  return localStorage.getItem('isAuthenticated') === 'true';
};

export const storeAccessToken = (token) => {
  localStorage.setItem('access_token', token);
};

export const getAccessToken = () => {
  return localStorage.getItem('access_token');
};

export const logoutUser = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('isAdmin');
  localStorage.removeItem('isAuthenticated');
  localStorage.removeItem('id')
  localStorage.removeItem('cart')
  store.dispatch('logout').then(() => {
    window.location.href = '/'
  })
};

export const refreshToken = async () => {
  try {
    const response = await axios.post('/api/auth/token/refresh', null, {
      withCredentials: true // Указывает, что куки (refresh-токен) должны быть отправлены с запросом
    });
    const { access_token } = response.data.access_token;
    storeAccessToken(access_token);
    storeUserInfo(access_token);
    return access_token;
  } catch (error) {
    toast.error('Ошибка обновления токена');
    throw error;
  }
};
