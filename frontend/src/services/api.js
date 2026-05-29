import axios from 'axios';

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
});

// Automatically attach JWT token to every request
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth
export const login = (data) => API.post('/auth/login', data);
export const register = (data) => API.post('/auth/register', data);

// Documents
export const uploadDocument = (formData) => API.post('/documents/upload', formData);
export const listDocuments = () => API.get('/documents/');
export const deleteDocument = (id) => API.delete(`/documents/${id}`);

// Query
export const queryPolicies = (question) => API.post('/query/', { question });

// Audit Logs
export const getMyAuditLogs = (page = 1, filters = {}) => {
  const params = new URLSearchParams({ page, page_size: 10, ...filters });
  return API.get(`/audit-logs/me?${params}`);
};

export const getAllAuditLogs = (page = 1, filters = {}) => {
  const params = new URLSearchParams({ page, page_size: 10, ...filters });
  return API.get(`/audit-logs/?${params}`);
};

// Users
export const getMe = () => API.get('/users/me');
export const listUsers = () => API.get('/users/');
export const updateUserRole = (id, role) => API.patch(`/users/${id}/role`, { role });