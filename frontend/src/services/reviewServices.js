import axios from "axios";
import { useToast } from 'vue-toastification'

const toast = useToast()

const API_URL = 'http://localhost:8000/api/reviews';

export const getToolReviews = async (id) => {
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

export const getAllReviews = async (filters={}) => {
  try{
    let url = `${API_URL}/paginated`
    if(Object.keys(filters).length > 0){
      url += '?'
      if (filters.tool_name){
        url += `&tool_name=${filters.tool_name}`
      }
      if (filters.reviewer_name){
        url += `&reviewer_name=${filters.reviewer_name}`
      }
      if (filters.reviewer_surname){
        url += `&reviewer_surname=${filters.reviewer_surname}`
      }
      if (filters.rating){
        url += `&rating=${filters.rating}`
      }
      if (filters.start_date){
        url += `&start_date=${filters.start_date}`
      }
      if (filters.end_date){
        url += `&end_date=${filters.end_date}`
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
}