// src/api/axios.js
import axios from "axios";

const API = axios.create({
  baseURL: "https://leroy-knifelike-grammatically.ngrok-free.dev/", // 🔁 cambia si tu backend está desplegado
  headers: {
    "Content-Type": "application/json",
    'ngrok-skip-browser-warning': 'true' // Puedes usar cualquier valor, 'true' es común
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
