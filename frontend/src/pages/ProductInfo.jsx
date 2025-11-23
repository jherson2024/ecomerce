import React, { useState } from "react";
import { Star, ShoppingCart } from "lucide-react";
import API from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function ProductInfo({ producto }) {
  const [loadingAdd, setLoadingAdd] = useState(false);
  const { usuario } = useAuth(); // ← usuario viene del AuthProvider

  const agregarCarrito = async () => {
    if (!usuario) {
      alert("Debes iniciar sesión para agregar productos al carrito.");
      return;
    }

    try {
      setLoadingAdd(true);

      await API.post(
        `/carrito/agregar?usuario_id=${usuario.id}&producto_id=${producto.id}&cantidad=1`
      );

      alert("Producto agregado al carrito ✔️");
    } catch (err) {
      console.error("Error al agregar al carrito", err);
      alert("No se pudo agregar al carrito");
    } finally {
      setLoadingAdd(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-semibold text-gray-900 mb-2">{producto.nombre}</h1>

      <div className="flex items-center gap-1 mb-4">
        {[...Array(5)].map((_, i) => (
          <Star
            key={i}
            size={18}
            className={
              i < Math.round(producto.promedio_puntuacion)
                ? "text-yellow-400 fill-yellow-400"
                : "text-gray-300"
            }
          />
        ))}
        <span className="text-sm text-gray-600 ml-2">
          {producto.promedio_puntuacion} de 5 ({producto.reseñas?.length || 0} reseñas)
        </span>
      </div>

      {producto.descuento_activo ? (
        <div className="mb-4">
          <p className="text-green-700 text-3xl font-semibold">
            S/ {(producto.precio - producto.precio * (producto.descuento_activo.valor / 100)).toFixed(2)}
            <span className="text-red-500 text-lg line-through ml-2">
              S/ {producto.precio.toFixed(2)}
            </span>
          </p>
        </div>
      ) : (
        <p className="text-green-700 text-3xl font-semibold mb-4">
          S/ {producto.precio.toFixed(2)}
        </p>
      )}

      <p className="text-gray-700 mb-6 leading-relaxed">{producto.descripcion}</p>

      <button
        onClick={agregarCarrito}
        disabled={loadingAdd}
        className="flex items-center gap-2 bg-green-700 hover:bg-green-800 text-white px-6 py-3 rounded-full transition font-medium disabled:bg-gray-400"
      >
        <ShoppingCart size={18} />
        {loadingAdd ? "Agregando..." : "Añadir al carrito"}
      </button>
    </div>
  );
}
