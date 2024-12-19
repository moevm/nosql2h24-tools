import axios from 'axios';
import { useToast } from 'vue-toastification'

const toast = useToast()

const API_URL = 'http://localhost:8000/api/data';

export const importData = async (json) => {
  try{
    const response = await axios.post(`${API_URL}/import`, json, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    toast.success("Данные успешно импортированы!")
    return "SUCCESS"
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage)
    return "ERROR"
  }
}

export const exportData = async () => {
  try{
    const response = await axios.get(`${API_URL}/export`);
    return response.data
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage)
    return "ERROR"
  }
}