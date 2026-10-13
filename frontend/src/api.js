import axios from 'axios';

const API_BASE = '/api';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach JWT token from localStorage
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('dsa_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  login: (username_or_email, password) =>
    api.post('/auth/login', { username_or_email, password }),
  register: (payload) => api.post('/auth/register', payload),
  getMe: () => api.get('/auth/me'),
  updateHandles: (payload) => api.put('/auth/handles', payload),
};

export const platformApi = {
  sync: () => api.post('/platforms/sync'),
  getStats: () => api.get('/platforms/stats'),
};

export const bktApi = {
  getMastery: () => api.get('/bkt/mastery'),
  submitVerdict: (payload) => api.post('/bkt/submit-verdict', payload),
  simulate: (payload) => api.post('/bkt/simulate', payload),
};

export const recApi = {
  getRecommendations: (params) => api.get('/recommendations', { params }),
};
