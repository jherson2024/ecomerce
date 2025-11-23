import React, { useEffect, useState } from "react";
import API from "../api/axios";
import ProductCard from "../components/ProductCard";
import { useSearch } from "../context/SearchContext";

function HomePage() {
  const { categoriaSeleccionada, searchQuery } = useSearch();
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchProductos = async (categoriaId = null, search = null) => {
    setLoading(true);
    try {
      let url;

      if (search && search.trim() !== "") {
        url = `/producto/buscar?q=${encodeURIComponent(search)}`;
      } else if (categoriaId) {
        url = `/producto/listar_por_categoria/${categoriaId}`;
      } else {
        url = "/producto/listar_disponibles";
      }

      const res = await API.get(url);
      setProductos(res.data);
    } catch (err) {
      console.error("Error cargando productos:", err);
      setProductos([]);
    } finally {
      setLoading(false);
    }
  };

  // 🔁 Escucha cambios de categoría o búsqueda
  useEffect(() => {
    fetchProductos(categoriaSeleccionada, searchQuery);
  }, [categoriaSeleccionada, searchQuery]);

  return (
    <div className="bg-neutral-50 min-h-screen">
      <main className="max-w-7xl mx-auto px-6 py-10">
        <h2 className="text-2xl font-bold text-green-900 mb-6">
          {searchQuery
            ? `Resultados para "${searchQuery}"`
            : categoriaSeleccionada
            ? "Productos por categoría"
            : "Productos destacados 🌱"}
        </h2>

        {loading ? (
          <p className="text-center text-gray-600 animate-pulse">
            Cargando productos...
          </p>
        ) : productos.length === 0 ? (
          <p className="text-center text-gray-500">
            No se encontraron productos.
          </p>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
            {productos.map((p) => (
              <ProductCard key={p.id} producto={p} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default HomePage;
