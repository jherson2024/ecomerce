import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import API from "../api/axios";
import { ArrowLeft } from "lucide-react";

export default function CollectionDetail() {
  const { vendedor_id, coleccion_id } = useParams();
  const [data, setData] = useState(null);

  useEffect(() => {
    API.get(`/tienda/${vendedor_id}/coleccion/${coleccion_id}`)
      .then((res) => setData(res.data))
      .catch((err) => console.error("Error:", err));
  }, [vendedor_id, coleccion_id]);

  if (!data) return <p className="text-center mt-10 animate-pulse">Cargando...</p>;

  const { coleccion, tienda, productos } = data;

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">

      <Link to={`/tienda/${vendedor_id}`} className="flex items-center gap-2 mb-6 text-gray-500 hover:text-black">
        <ArrowLeft size={20} />
        Volver a la tienda
      </Link>

      {/* Encabezado */}
      <div className="bg-white p-6 rounded-xl shadow mb-8">
        <h1 className="text-3xl font-bold">{coleccion.nombre}</h1>
        <p className="text-gray-600">{coleccion.descripcion}</p>
      </div>

      {/* Productos */}
      <h2 className="text-2xl font-semibold mb-4">Productos</h2>
      <div className="grid md:grid-cols-4 gap-6">
        {productos.map((p) => (
          <Link
            key={p.id}
            to={`/producto/${p.id}`}
            className="bg-white p-4 rounded-xl shadow hover:shadow-lg transition"
          >
            <img
              src={p.imagen}
              className="w-full h-40 object-cover rounded-lg"
            />
            <h4 className="font-semibold mt-2">{p.nombre}</h4>
            <p className="text-blue-600 font-bold">S/ {p.precio}</p>
          </Link>
        ))}
      </div>

    </div>
  );
}
