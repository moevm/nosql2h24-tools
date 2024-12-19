import axios from "axios";
import { useToast } from 'vue-toastification'

const toast = useToast()

const API_URL = 'http://localhost:8000/api/workers';

export const getWorkers = async (filters={}) => {
  try{
    let url = `${API_URL}/paginated/`
    if(Object.keys(filters).length > 0){
      console.log(filters)
      url += '?'
      if(filters.name){
        url += `&name=${filters.name}`
      }
      if(filters.surname){
        url += `&surname=${filters.surname}`
      }
      if(filters.jobTitle){
        url += `&jobTitle=${filters.jobTitle}`
      }
      if(filters.email){
        url += `&email=${filters.email}`
      }
      if(filters.phone){
        url += `&phone=${filters.phone}`
      }
    }
    const response = await axios.get(url);
    if(Object.keys(filters).length > 0){
      toast.success("Фильтры успешно применены!")
    }
    return response.data
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage)
    return "ERROR"
  }
}
