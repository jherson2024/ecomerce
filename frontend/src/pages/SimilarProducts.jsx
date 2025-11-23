import React from "react";
import ProductCard from "./ProductCard";

export default function SimilarProducts({ productos }) {
  if (!productos?.length) {
    return (
      <section className="my-0">
        <p>.</p>
      </section>
    );
  }
  return (
    <section className="my-0">
      <h2 className="text-lg font-bold text-gray-900 mb-3">Artículos similares</h2>
      <div className="flex gap-4 overflow-x-auto pb-2">
        {productos.map((p) => (
          <div key={p.id} className="min-w-[180px]">
            <ProductCard producto={p} />
          </div>
        ))}
      </div>
    </section>
  );
}
