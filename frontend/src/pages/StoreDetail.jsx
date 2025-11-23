import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import API from "../api/axios";
import { ArrowLeft } from "lucide-react";

export default function StoreDetail() {
  const { vendedor_id } = useParams();
  const [tienda, setTienda] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStore = async () => {
      try {
        const res = await API.get(`/tienda/detalle/${vendedor_id}`);
        setTienda(res.data);
      } catch (err) {
        console.error("Error cargando la tienda", err);
      } finally {
        setLoading(false);
      }
    };
    fetchStore();
  }, [vendedor_id]);

  if (loading) return <p className="text-center mt-10 animate-pulse">Cargando tienda...</p>;
  if (!tienda) return <p className="text-center mt-10">Tienda no encontrada.</p>;

  const info = tienda.tienda;

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">

      <Link to="/" className="flex items-center gap-2 mb-6 text-gray-500 hover:text-black">
        <ArrowLeft size={20} />
        Volver
      </Link>

      {/* Info principal */}
      <div className="flex items-center gap-6 bg-white shadow p-6 rounded-xl">
        <img
          src={info.logo}
          alt={info.nombre}
          className="w-28 h-28 object-cover rounded-full border"
        />

        <div>
          <h1 className="text-3xl font-bold">{info.nombre}</h1>
          <p className="text-gray-600">{info.descripcion}</p>
          <p className="mt-2 text-sm text-gray-500">{info.ubicacion}</p>
        </div>
      </div>

      {/* Colecciones */}
      <h2 className="text-2xl font-semibold mt-10 mb-4">Colecciones</h2>

      <div className="grid md:grid-cols-3 gap-6">
        {tienda.colecciones.map((c) => (
            <Link
            to={`/tienda/${info.id}/coleccion/${c.id}`}
            key={c.id}
            className="bg-white p-4 rounded-xl shadow hover:shadow-xl transition block"
            >
            {/* Collage */}
            <div className="grid grid-cols-2 gap-2 mb-4">
              {c.imagenes && c.imagenes.length > 0 ? (
                c.imagenes.map((img, i) => (
                  <img
                    key={i}
                    src={img}
                    className="w-full h-24 object-cover rounded-lg"
                    alt={`imagen collage ${i}`}
                  />
                ))
              ) : (
                <div className="col-span-2 text-center text-gray-400 text-sm py-6">
                  Sin imágenes
                </div>
              )}
            </div>

            <h3 className="font-bold">{c.nombre}</h3>
            <p className="text-sm text-gray-600">{c.descripcion}</p>
          </Link>
        ))}
      </div>

      {/* Productos */}
      <h2 className="text-2xl font-semibold mt-10 mb-4">Productos</h2>

      <div className="grid md:grid-cols-4 gap-6">
        {tienda.productos.map((p) => (
          <Link
            to={`/producto/${p.id}`}
            key={p.id}
            className="bg-white p-4 rounded-xl shadow hover:shadow-lg"
          >
            <img src={p.imagen} alt={p.nombre} className="w-full h-40 object-cover rounded-lg" />
            <h4 className="font-semibold mt-2">{p.nombre}</h4>
            <p className="text-blue-600 font-bold text-lg">S/ {p.precio}</p>
          </Link>
        ))}
      </div>

      {/* Políticas */}
      <h2 className="text-2xl font-semibold mt-10 mb-4">Políticas</h2>
      <div className="bg-white p-6 rounded-xl shadow">
        <p><strong>Envío:</strong> {info.politicas.envio}</p>
        <p className="mt-2"><strong>Devolución:</strong> {info.politicas.devolucion}</p>
        <p className="mt-2"><strong>Privacidad:</strong> {info.politicas.privacidad}</p>
      </div>

    </div>
  );
}
