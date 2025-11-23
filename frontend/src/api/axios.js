// src/api/axios.js
import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000", // 🔁 cambia si tu backend está desplegado
  headers: {
    "Content-Type": "application/json",
  },
});

// (Opcional) Interceptor para incluir token o manejar errores globales
API.interceptors.request.use((config) => {
  const usuario = JSON.parse(localStorage.getItem("usuarioAdmin"));
  if (usuario?.token) {
    config.headers.Authorization = `Bearer ${usuario.token}`;
  }
  return config;
});

export default API;
