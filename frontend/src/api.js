import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to attach auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;

export const propertyService = {
  getProperties: (params) => api.get('/properties/', { params }),
  getProperty: (id) => api.get(`/properties/${id}/`),
  getFeaturedProperties: () => api.get('/properties/featured/'),
};

export const aiService = {
  chat: (message, sessionId) => api.post('/ai/chat/', { message, session_id: sessionId }),
  estimateValue: (data) => api.post('/ai/estimate-value/', data),
};
