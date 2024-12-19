import axios from 'axios';
import { useToast } from 'vue-toastification'

const toast = useToast()

const API_URL = 'http://localhost:8000/api/orders';

export const createOrder = async (userData) => {
  try{
    const response = await axios.post(`${API_URL}/${localStorage.getItem("id")}`, userData, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    toast.success("Заказ успешно создан!")
    return "SUCCESS"
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage)
    return "ERROR"
  }
}

export const getClientOrders = async (filters={}) => {
  try{
    let url = `${API_URL}/client/paginated/${localStorage.getItem("id")}`
    if(Object.keys(filters).length > 0){
      url += '?'
      if(filters.tool_name){
        url += `&tool_name=${filters.tool_name[0]}`
      }
      if(filters.start_date){
        url += `&start_date=${filters.start_date}`
      }
      if(filters.end_date){
        url += `&end_date=${filters.end_date}`
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

export const getOrderData = async (id) => {
  try{
    console.log(id)
    const response = await axios.get(`${API_URL}/${id}`);
    console.log(response)
    return response.data
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage)
    return "ERROR"
  }
};

export const getAllOrders = async (filters={}) => {
  try{
    let url = `${API_URL}/worker/paginated`
    if(Object.keys(filters).length > 0){
      url += '?'
      if(filters.tool_name){
        url += `&tool_name=${filters.tool_name[0]}`
      }
      if(filters.start_date){
        url += `&start_date=${filters.start_date}`
      }
      if(filters.end_date){
        url += `&end_date=${filters.end_date}`
      }
      if(filters.min_price){
        url += `&min_price=${filters.min_price}`
      }
      if(filters.max_price){
        url += `&max_price=${filters.max_price}`
      }
      if(filters.customer_name) {
        url += `&customer_name=${filters.customer_name}`
      }
      if(filters.customer_surname) {
        url += `&customer_surname=${filters.customer_surname}`
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