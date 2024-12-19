import axios from 'axios';
import { useToast } from 'vue-toastification'

const toast = useToast()

const API_URL = 'http://localhost:8000/api/tools';

export const getSearchTools = async (search, filters={}) => {
  try{
    let url = `${API_URL}/search?query=${search}`
    if(Object.keys(filters).length > 0){
      if(filters.category){
        filters.category.map((elem) => {
          url += `&category=${elem}`
        })
      }
      if(filters.type){
        filters.type.map((elem) => {
          url += `&type=${elem}`
        })
      }
      if(filters.min_price){
        url += `&min_price=${filters.min_price}`
      }
      if(filters.max_price){
        url += `&max_price=${filters.max_price}`
      }
      url += `&page=${filters.page}`
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

export const getToolDetails = async (id) => {
  try{
    const response = await axios.get(`${API_URL}/${id}`);
    return response.data
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage)
    return "ERROR"
  }
}
