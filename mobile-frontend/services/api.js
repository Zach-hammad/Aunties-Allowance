import axios from 'axios';
import * as SecureStore from 'expo-secure-store';  // ✅ Correct way now!

const API_BASE_URL = 'http://10.250.102.152:5000';  // ✅ Localhost for testing

// Create base axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Attach token automatically before every request
apiClient.interceptors.request.use(
  async (config) => {
    const token = await SecureStore.getItemAsync('accessToken');  // ✅ Pull securely

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;
