import axios from 'axios';
import {jwtDecode} from "jwt-decode";
import store from "@/js/store.js";

const API_URL = 'http://localhost:3000/api/auth';

export const register = async (userData) => {
  try{
    const response = await axios.post(`${API_URL}/register/client`, userData);
    return { data: response.data, error: null};
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    return { data: null, error: errorMessage}
  }
};

export const login = async (userData) => {
  try{
    const response = await axios.post(`${API_URL}/token`, userData);
    return { data: response.data, error: null}
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    return { data: null, error: errorMessage}
  }
};

export const storeUserInfo = (token) => {
  storeAccessToken(token);
  const decodedToken = jwtDecode(token);
  const isAdmin = (decodedToken.role === "admin") || false;
  const isAuthenticated = true;

  localStorage.setItem('isAdmin', isAdmin.toString());
  localStorage.setItem('isAuthenticated', isAuthenticated.toString());
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
};

export const refreshToken = async () => {
  try {
    const response = await axios.post('/api/auth/token/refresh', null, {
      withCredentials: true // Указывает, что куки (refresh-токен) должны быть отправлены с запросом
    });
    const { access_token } = response.data;
    storeAccessToken(access_token);
    storeUserInfo(access_token);
    return access_token;
  } catch (error) {
    console.error('Ошибка обновления токена:', error);
    throw error;
  }
};
