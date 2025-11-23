import React, { useState } from "react";
import API from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function AuthModal({ open, onClose }) {
  const [tab, setTab] = useState("login");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  if (!open) return null;

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    const email = e.target.email.value;
    const clave = e.target.clave.value;

    try {
      const res = await API.post("/auth/login", { email, clave });
      login(res.data.usuario, res.data.token);
      onClose();
    } catch {
      alert("Credenciales incorrectas");
    }

    setLoading(false);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);

    const nombre = e.target.nombre.value;
    const email = e.target.email.value;
    const clave = e.target.clave.value;

    try {
      await API.post("/auth/register", { nombre, email, clave });
      alert("Registro exitoso, inicia sesión.");
      setTab("login");
    } catch {
      alert("Error registrando usuario");
    }

    setLoading(false);
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/40 z-[99999] backdrop-blur-sm">

      <div className="w-[720px] bg-white rounded-3xl shadow-xl flex overflow-hidden border border-gray-100 relative">

        {/* Cerrar */}
        <button
          onClick={onClose}
          className="absolute right-4 top-4 text-gray-500 hover:text-gray-700 text-xl"
        >
          ✕
        </button>

        {/* IZQUIERDA */}
        <div className="w-[40%] p-6 bg-gradient-to-b from-green-600 to-green-700 text-white flex flex-col justify-center rounded-r-[40px]">
          <h1 className="text-xl font-extrabold leading-snug mb-3">
            Gestiona tus compras<br />con facilidad.
          </h1>

          <p className="text-green-100 text-xs max-w-xs mb-6">
            Encuentra los mejores productos y agroquímicos en nuestra tienda agrícola.
          </p>

          <img
            src="https://cdn-icons-png.flaticon.com/512/891/891462.png"
            alt="shopping cart"
            className="w-36 mx-auto opacity-90 drop-shadow-xl"
          />
        </div>

        {/* DERECHA */}
        <div className="w-[60%] p-8">

          <div className="flex items-center gap-2 mb-5">
            <div className="text-3xl">🌾</div>
            <h2 className="text-xl font-bold">AgroMarket</h2>
          </div>

          <h2 className="text-2xl font-bold text-gray-800 mb-1">
            {tab === "login" ? "Bienvenido" : "Crear cuenta"}
          </h2>

          <p className="text-gray-500 mb-5 text-xs">
            {tab === "login" ? "Inicia sesión para continuar" : "Regístrate para comenzar"}
          </p>

          {/* FORMULARIO CORREGIDO */}
          <form
            onSubmit={tab === "login" ? handleLogin : handleRegister}
            className="space-y-3"
          >

            {tab === "register" && (
              <input
                name="nombre"
                type="text"
                placeholder="Nombre completo"
                className="w-full border rounded-xl bg-gray-50 p-2.5 text-sm outline-none focus:ring-2 focus:ring-green-600"
              />
            )}

            <input
              name="email"
              type="email"
              placeholder="Correo electrónico"
              className="w-full border rounded-xl bg-gray-50 p-2.5 text-sm outline-none focus:ring-2 focus:ring-green-600"
              required
            />

            <input
              name="clave"
              type="password"
              placeholder="Contraseña"
              className="w-full border rounded-xl bg-gray-50 p-2.5 text-sm outline-none focus:ring-2 focus:ring-green-600"
              required
            />

            <button
              type="submit"
              className="w-full bg-green-600 hover:bg-green-700 transition text-white py-2.5 rounded-xl text-sm font-semibold shadow"
            >
              {tab === "login"
                ? loading ? "Ingresando..." : "Ingresar"
                : loading ? "Registrando..." : "Registrarse"}
            </button>
          </form>

          {/* Separator */}
          <div className="flex items-center my-4 gap-2">
            <div className="flex-1 h-px bg-gray-200" />
            <span className="text-gray-400 text-xs">o continuar con</span>
            <div className="flex-1 h-px bg-gray-200" />
          </div>

          {/* Social buttons */}
          <div className="flex gap-2 mb-3">
            <button className="flex-1 border rounded-xl py-2 bg-white flex items-center justify-center gap-2 hover:bg-gray-50 text-xs">
              <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg" className="w-4" />
              Google
            </button>

            <button className="flex-1 border rounded-xl py-2 bg-white flex items-center justify-center gap-2 hover:bg-gray-50 text-xs">
              <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/facebook/facebook-original.svg" className="w-4" />
              Facebook
            </button>
          </div>

          {/* Cambio de tab */}
          <p className="text-center text-xs text-gray-600">
            {tab === "login"
              ? <>¿No tienes cuenta? <span onClick={() => setTab("register")} className="text-green-600 font-semibold cursor-pointer">Regístrate</span></>
              : <>¿Ya tienes cuenta? <span onClick={() => setTab("login")} className="text-green-600 font-semibold cursor-pointer">Inicia sesión</span></>
            }
          </p>

        </div>
      </div>
    </div>
  );
}
