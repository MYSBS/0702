import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const sendMessage = async (message, carModel) => {
  try {
    const response = await axios.post(`${API_URL}/chat`, {
      message: message,
      car_model: carModel,
    });
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};
