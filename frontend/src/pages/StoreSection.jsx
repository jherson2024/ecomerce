import React from "react";
import { Link } from "react-router-dom";

export default function StoreSection({ tienda }) {
  if (!tienda) return null;

  return (
    <section className="mt-16 border-t pt-10">
      <Link
        to={`/tienda/${tienda.id}`}
        className="flex items-center gap-4 mb-6 hover:opacity-80 transition"
      >
        {tienda.logo && (
          <img
            src={tienda.logo}
            alt={tienda.nombre_tienda}
            className="w-16 h-16 rounded-full object-cover border"
          />
        )}

        <div>
          <h3 className="text-xl font-bold text-gray-900">{tienda.nombre_tienda}</h3>
          <p className="text-gray-700 mt-2">{tienda.descripcion}</p>
        </div>
      </Link>
    </section>
  );
}
