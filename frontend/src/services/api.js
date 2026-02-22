import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

// Cities
export const citiesAPI = {
  search: (query) => api.get('/cities', { params: { search: query } }),
  getAll: () => api.get('/cities'),
  getById: (id) => api.get(`/cities/${id}`),
};

// Products
export const productsAPI = {
  search: (query, cityId) => api.get('/products/search', { params: { q: query, city_id: cityId } }),
  getById: (id) => api.get(`/products/${id}`),
  getHistory: (id, cityId, days = 30) => api.get(`/products/${id}/history`, { params: { city_id: cityId, days } }),
};

// Supermarkets
export const supermarketsAPI = {
  getAll: (cityId) => api.get('/supermarkets', { params: { city_id: cityId } }),
  getById: (id) => api.get(`/supermarkets/${id}`),
};

// Offers
export const offersAPI = {
  getOffers: (productId, cityId) => api.get('/offers', { params: { product_id: productId, city_id: cityId } }),
  create: (data) => api.post('/offers', data),
};

// Users
export const usersAPI = {
  getFavorites: () => api.get('/users/me/favorites'),
  addFavorite: (entityType, entityId) => api.post('/users/me/favorites', null, { params: { entity_type: entityType, entity_id: entityId } }),
  removeFavorite: (entityType, entityId) => api.delete(`/users/me/favorites/${entityType}/${entityId}`),
  
  getAlerts: () => api.get('/users/me/alerts'),
  createAlert: (data) => api.post('/users/me/alerts', data),
  deleteAlert: (id) => api.delete(`/users/me/alerts/${id}`),
};

export default api;
