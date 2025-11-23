import React from "react";
import { Link } from "react-router-dom";

function ProductCard({ producto }) {
  return (
    <Link
      to={`/producto/${producto.id}`}
      className="bg-white rounded-2xl shadow hover:shadow-lg transition-all hover:scale-[1.02] overflow-hidden"
    >
      <img
        src={producto.imagen || "/images/no-image.png"}
        alt={producto.nombre}
        className="w-full h-48 object-cover"
      />
      <div className="p-3">
        <h3 className="text-green-900 font-semibold text-sm truncate">
          {producto.nombre}
        </h3>
        <p className="text-green-700 font-bold mt-1 text-base">
          ${producto.precio.toFixed(2)}
        </p>
      </div>
    </Link>
  );
}

export default ProductCard;
