import axios from 'axios';
import { useToast } from 'vue-toastification'

const toast = useToast()

const API_URL = 'http://localhost:8000/api/clients';


export const getProfileData = async (id=0) => {
  try{
    let url = ''
    if(id){
      url = `${API_URL}/${id}/private`
    }
    else {
      url = `${API_URL}/${localStorage.getItem('id')}/private`
    }
    const response = await axios.get(url);
    return response.data
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage)
    return "ERROR"
  }
};

export const updateProfileData = async (profileData) => {
  try{
    const response = await axios.patch(`${API_URL}/${localStorage.getItem('id')}`, profileData, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    toast.success("Данные успешно обновлены!")
    return "SUCCESS"
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage)
    return "ERROR"
  }
}

export const changePassword = async (formData) => {
  try{
    const response = await axios.patch(`${API_URL}/${localStorage.getItem('id')}/password`, formData, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    toast.success("Пароль успешно обновлен!")
    return "SUCCESS"
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage)
    return "ERROR"
  }
}