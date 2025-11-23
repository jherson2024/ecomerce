import React from "react";
import { Star, Sparkles } from "lucide-react";

export default function ProductReviews({ reseñas = [] }) {
  const promedio =
    reseñas.length > 0
      ? (
          reseñas.reduce((acc, r) => acc + r.puntuacion, 0) / reseñas.length
        ).toFixed(1)
      : 0;

  return (
    <section className="text-gray-800">
      {/* ⭐ Encabezado principal */}
      <div className="flex items-center gap-2 mb-1">
        <Star className="text-yellow-500 fill-yellow-500" size={20} />
        <span className="text-lg font-semibold">{promedio} de 5</span>
        <span className="text-gray-500 text-sm">
          ({reseñas.length} reseñas)
        </span>
      </div>
      <p className="text-sm text-gray-500 mb-6">
        Todas las reseñas son de compradores verificados
      </p>

      {/* ✨ Resumen por IA */}
      <div className="mb-6 border-t pt-4">
        <div className="flex items-center gap-2 mb-3">
          <Sparkles className="text-green-700" size={16} />
          <p className="font-medium text-gray-700 text-sm">
            Datos de los compradores, resumidos automáticamente
          </p>
        </div>
        <div className="flex flex-wrap gap-2 text-sm text-gray-700">
          {[
            "Justo lo que quería",
            "Fiel a la descripción",
            "Buena calidad",
            "Queda genial",
            "Fácil de usar",
          ].map((tag, i) => (
            <span
              key={i}
              className="px-3 py-1 border border-gray-300 rounded-full bg-gray-50 hover:bg-gray-100 cursor-default"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>

      {/* 🗣️ Lista de reseñas */}
      <div className="divide-y">
        {reseñas.length > 0 ? (
          reseñas.map((r, i) => (
            <div key={i} className="py-5 first:pt-0 last:pb-0">
              {/* Estrellas + etiquetas */}
              <div className="flex items-center gap-1 mb-2">
                {[...Array(r.puntuacion)].map((_, idx) => (
                  <Star
                    key={idx}
                    size={16}
                    className="text-yellow-400 fill-yellow-400"
                  />
                ))}
                <span className="ml-2 text-xs font-medium text-green-700 bg-green-50 border border-green-200 px-2 py-0.5 rounded-full">
                  Este artículo
                </span>
                <span className="text-xs text-gray-500 ml-2">
                  ✓ Lo recomienda
                </span>
              </div>

              {/* Comentario */}
              <p className="text-gray-800 mb-2 leading-relaxed">
                {r.comentario}
              </p>

              {/* Usuario + Fecha */}
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center text-[10px] font-semibold text-green-800">
                  {r.usuario.charAt(0)}
                </div>
                <p className="text-sm font-medium text-gray-700">
                  {r.usuario}
                </p>
                <span className="text-xs text-gray-500 ml-auto">{r.fecha}</span>
              </div>
            </div>
          ))
        ) : (
          <p className="text-gray-500 text-sm italic py-6">
            Aún no hay reseñas para este artículo.
          </p>
        )}
      </div>
    </section>
  );
}
