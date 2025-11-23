import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API from "../api/axios";
import { ShoppingCart, Search, User } from "lucide-react";
import { useSearch } from "../context/SearchContext";
import { useAuth } from "../context/AuthContext";
import AuthModal from "./AuthModal";

function Navbar() {
  const [categorias, setCategorias] = useState([]);
  const [search, setSearch] = useState("");
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [carritoCount, setCarritoCount] = useState(0);

  const { usuario, logout } = useAuth();
  const { setSearchQuery, setCategoriaSeleccionada } = useSearch();
  const navigate = useNavigate();

  // ============================
  //   CARGAR CATEGORÍAS
  // ============================
  useEffect(() => {
    const fetchCategorias = async () => {
      try {
        const res = await API.get("/producto/listar_categorias");
        setCategorias(res.data);
      } catch (err) {
        console.error("Error cargando categorías", err);
      }
    };
    fetchCategorias();
  }, []);

  // ============================
  //   CARGAR CARRITO DEL USUARIO
  // ============================
  useEffect(() => {
    const fetchCarrito = async () => {
      if (!usuario) {
        setCarritoCount(0);
        return;
      }

      try {
        const res = await API.get(`/carrito/obtener/${usuario.id}`);
        setCarritoCount(res.data.detalles.length);
      } catch (err) {
        console.error("Error cargando carrito", err);
        setCarritoCount(0);
      }
    };

    fetchCarrito();
  }, [usuario]);

  // ============================
  //  BUSCAR PRODUCTOS
  // ============================
  const handleSubmit = (e) => {
    e.preventDefault();
    setCategoriaSeleccionada(null);
    setSearchQuery(search.trim() || null);
    navigate("/");
  };

  const handleCategoriaClick = (id) => {
    setCategoriaSeleccionada(id);
    setSearchQuery(null);
    navigate("/");
  };

  return (
    <>
      {/* NAVBAR */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto flex justify-between items-center p-2">

          {/* LOGO */}
          <Link
            to="/"
            className="text-2xl font-extrabold text-green-700"
            onClick={() => {
              setCategoriaSeleccionada(null);
              setSearchQuery(null);
            }}
          >
            🌾 AgroMarket
          </Link>

          {/* SEARCH */}
          <form
            onSubmit={handleSubmit}
            className="flex items-center w-full max-w-md border border-gray-300 rounded-full px-4 py-2 bg-gray-50"
          >
            <Search className="text-gray-500 mr-2" size={18} />
            <input
              type="text"
              placeholder="Buscar productos agroquímicos..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-transparent outline-none text-sm"
            />
          </form>

          {/* ICONOS */}
          <div className="flex items-center gap-5">

            {/* PERFIL */}
            {!usuario ? (
              <button
                onClick={() => setAuthModalOpen(true)}
                className="text-gray-700 hover:text-green-700"
              >
                <User size={22} />
              </button>
            ) : (
              <div className="relative group">
                <button className="text-gray-700 hover:text-green-700">
                  <User size={22} />
                </button>

                {/* MENÚ PERFIL */}
                <div className="absolute right-0 mt-0 bg-white border rounded shadow-lg p-3 w-40 hidden group-hover:block">
                  <p className="font-medium text-gray-800">{usuario.nombre}</p>

                  <Link
                    to="/perfil"
                    className="block mt-2 text-sm text-green-700 hover:underline"
                  >
                    Ver perfil
                  </Link>

                  {/* NUEVA OPCIÓN: PEDIDOS */}
                  <Link
                    to="/pedidos"
                    className="block mt-2 text-sm text-green-700 hover:underline"
                  >
                    Mis pedidos
                  </Link>

                  <button
                    onClick={logout}
                    className="mt-2 text-sm text-red-600 hover:underline"
                  >
                    Cerrar sesión
                  </button>
                </div>
              </div>
            )}

            {/* CARRITO */}
            <Link to="/carrito" className="text-gray-700 hover:text-green-700 relative">
              <ShoppingCart size={22} />
              {carritoCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-green-700 text-white text-xs px-1.5 py-0.5 rounded-full">
                  {carritoCount}
                </span>
              )}
            </Link>

          </div>
        </div>

        {/* CATEGORÍAS */}
        <nav className="bg-green-50 border-t border-gray-100">
          <div className="max-w-7xl mx-auto flex gap-5 overflow-x-auto px-6 py-2 text-sm text-green-800">
            <button
              onClick={() => handleCategoriaClick(null)}
              className="hover:text-green-700 whitespace-nowrap font-medium"
            >
              Todos
            </button>
            {categorias.map((cat) => (
              <button
                key={cat.id}
                onClick={() => handleCategoriaClick(cat.id)}
                className="hover:text-green-700 whitespace-nowrap"
              >
                {cat.nombre}
              </button>
            ))}
          </div>
        </nav>
      </header>

      {/* MODAL LOGIN/REGISTER */}
      <AuthModal open={authModalOpen} onClose={() => setAuthModalOpen(false)} />
    </>
  );
}
export default Navbar;
