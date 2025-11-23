import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API from "../api/axios";

function CategoryList({ titulo = "Categorías destacadas" }) {
  const [categorias, setCategorias] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCategorias = async () => {
      try {
        const res = await API.get("/producto/listar_categorias");
        setCategorias(res.data);
      } catch (err) {
        console.error("Error al cargar categorías:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchCategorias();
  }, []);

  if (loading)
    return (
      <p className="text-center text-gray-500 mt-5 animate-pulse">
        Cargando categorías...
      </p>
    );

  if (categorias.length === 0)
    return <p className="text-center text-gray-500 mt-5">No hay categorías disponibles.</p>;

  return (
    <section className="mt-10">
      <h2 className="text-2xl font-bold text-green-900 mb-6">{titulo}</h2>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-5">
        {categorias.map((cat) => (
          <Link
            key={cat.id}
            to={`/categoria/${cat.id}`}
            className="group bg-white border border-gray-200 rounded-2xl shadow-sm hover:shadow-md hover:scale-[1.02] transition-all p-4 flex flex-col items-center text-center"
          >
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-3 group-hover:bg-green-200 transition">
              <img
                src={`/icons/${cat.nombre.toLowerCase()}.png`}
                alt={cat.nombre}
                onError={(e) => {
                  e.target.src = "/icons/default.png"; // ícono genérico si no hay imagen
                }}
                className="w-8 h-8 object-contain opacity-80"
              />
            </div>
            <h3 className="text-green-900 font-semibold text-sm">{cat.nombre}</h3>
            {cat.descripcion && (
              <p className="text-gray-500 text-xs mt-1 line-clamp-2">
                {cat.descripcion}
              </p>
            )}
          </Link>
        ))}
      </div>
    </section>
  );
}

export default CategoryList;
