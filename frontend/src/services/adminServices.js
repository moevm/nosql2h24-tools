import axios from 'axios';
import { useToast } from 'vue-toastification'

const toast = useToast()
const API_URL = 'http://localhost:8000/api';

export const getTools = async (page=1) => {
  try{
    const response = await axios.get(`${API_URL}/tools/paginated/?page=${page}`)
    return response.data
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage);
    return "ERROR"
  }
}

export const getToolsPagesCount = async () => {
  try{
    const response = await axios.get(`${API_URL}/tools/pages_count`)
    return response.data
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage);
    return "ERROR"
  }
}

export const getEmployees = async (data) => {

}

export const addNewCategory = async (userData) => {
  try{
    const response = await axios.post(`${API_URL}/categories/`, userData, {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
    toast.success("Категория успешно добавлена!")
    return "SUCCESS"
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage);
    return "ERROR"
  }
}

export const addNewTool = async (userData) => {
  try{
    const response = await axios.post(`${API_URL}/tools/`, userData, {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
    toast.success("Инструмент успешно добавлен!")
    return "SUCCESS"
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage);
    return "ERROR"
  }
}

export const getAllCategories = async () => {
  try{
    const response = await axios.get(`${API_URL}/categories/with_types`)
    return response.data
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage);
    return "ERROR"
  }
}

export const addNewType = async (userData) => {
  try{
    const response = await axios.post(`${API_URL}/types/`, userData, {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
    toast.success("Тип успешно добавлен!")
    return "SUCCESS"
  } catch (error) {
    const errorMessage = error.response
      ? error.response.data.message // Если есть ответ от сервера
      : error.message || 'Ошибка соединения';
    toast.error(errorMessage);
    return "ERROR"
  }
}

// {
//   image: "https://cdnstatic.rg.ru/crop800x800/uploads/images/2023/09/08/photo_3_2023-09-08_11-30-34_893.jpg",
//     title: "Название инструмента",
//   description: "Краткое описание инструмента",
//   id: "1",
//   rating: "3",
//   dailyPrice: "10000",
// },
// {
//   image: "https://cdnstatic.rg.ru/crop800x800/uploads/images/2023/09/08/photo_3_2023-09-08_11-30-34_893.jpg",
//     title: "Название инструмента",
//   description: "Краткое описание инструмента",
//   id: "2",
//   rating: "3",
//   dailyPrice: "10000",
// },
// {
//   image: "https://cdnstatic.rg.ru/crop800x800/uploads/images/2023/09/08/photo_3_2023-09-08_11-30-34_893.jpg",
//     title: "Название инструмента",
//   description: "Краткое описание инструмента",
//   id: "3",
//   rating: "3",
//   dailyPrice: "10000",
// },
// {
//   image: "https://cdnstatic.rg.ru/crop800x800/uploads/images/2023/09/08/photo_3_2023-09-08_11-30-34_893.jpg",
//     title: "Название инструмента",
//   description: "Краткое описание инструмента",
//   id: "4",
//   rating: "3",
//   dailyPrice: "10000",
// },
// {
//   image: "https://cdnstatic.rg.ru/crop800x800/uploads/images/2023/09/08/photo_3_2023-09-08_11-30-34_893.jpg",
//     title: "Название инструмента",
//   description: "Краткое описание инструмента",
//   id: "5",
//   rating: "3",
//   dailyPrice: "10000",
// },
// {
//   image: "https://cdnstatic.rg.ru/crop800x800/uploads/images/2023/09/08/photo_3_2023-09-08_11-30-34_893.jpg",
//     title: "Название инструмента",
//   description: "Краткое описание инструмента",
//   id: "6",
//   rating: "3",
//   dailyPrice: "10000",
// },
// {
//   image: "https://cdnstatic.rg.ru/crop800x800/uploads/images/2023/09/08/photo_3_2023-09-08_11-30-34_893.jpg",
//     title: "Название инструмента",
//   description: "Краткое описание инструмента",
//   id: "7",
//   rating: "3",
//   dailyPrice: "10000",
// },
// {
//   image: "https://cdnstatic.rg.ru/crop800x800/uploads/images/2023/09/08/photo_3_2023-09-08_11-30-34_893.jpg",
//     title: "Название инструмента",
//   description: "Краткое описание инструмента",
//   id: "8",
//   rating: "3",
//   dailyPrice: "10000",
// },
// {
//   image: "https://cdnstatic.rg.ru/crop800x800/uploads/images/2023/09/08/photo_3_2023-09-08_11-30-34_893.jpg",
//     title: "Название инструмента",
//   description: "Краткое описание инструмента",
//   id: "9",
//   rating: "3",
//   dailyPrice: "10000",
// },
// {
//   image: "https://cdnstatic.rg.ru/crop800x800/uploads/images/2023/09/08/photo_3_2023-09-08_11-30-34_893.jpg",
//     title: "Название инструмента",
//   description: "Краткое описание инструмента",
//   id: "10",
//   rating: "3",
//   dailyPrice: "10000",
// },
// {
//   image: "https://cdnstatic.rg.ru/crop800x800/uploads/images/2023/09/08/photo_3_2023-09-08_11-30-34_893.jpg",
//     title: "Название инструмента",
//   description: "Краткое описание инструмента",
//   id: "11",
//   rating: "3",
//   dailyPrice: "10000",
// },
// {
//   image: "https://cdnstatic.rg.ru/crop800x800/uploads/images/2023/09/08/photo_3_2023-09-08_11-30-34_893.jpg",
//     title: "Название инструмента",
//   description: "Краткое описание инструмента",
//   id: "12",
//   rating: "3",
//   dailyPrice: "10000",
// },