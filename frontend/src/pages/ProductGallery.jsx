import React from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

export default function ProductGallery({ imagenes, imagenIndex, cambiarImagen, setImagenIndex, nombre }) {
  return (
    <div className="flex gap-4">
      <div className="flex flex-col gap-3">
        {imagenes.map((img, idx) => (
          <img
            key={idx}
            src={img}
            alt={`Vista ${idx + 1}`}
            onClick={() => setImagenIndex(idx)}
            className={`w-16 h-16 rounded-lg object-cover border cursor-pointer transition ${
              idx === imagenIndex ? "border-green-700" : "border-gray-200"
            }`}
          />
        ))}
      </div>

      <div className="relative flex-1 flex justify-center items-center">
        <button
          onClick={() => cambiarImagen("prev")}
          className="absolute left-2 bg-white/80 hover:bg-white rounded-full p-1 shadow"
        >
          <ChevronLeft size={20} />
        </button>
        <img
          src={imagenes[imagenIndex]}
          alt={nombre}
          className="rounded-xl w-full max-h-[450px] object-contain"
        />
        <button
          onClick={() => cambiarImagen("next")}
          className="absolute right-2 bg-white/80 hover:bg-white rounded-full p-1 shadow"
        >
          <ChevronRight size={20} />
        </button>
      </div>
    </div>
  );
}
