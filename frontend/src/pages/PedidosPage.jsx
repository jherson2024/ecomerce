import React, { useEffect, useState } from "react";
import API from "../api/axios";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";
import { ESTADO_COLORES } from "../utils/EstadoStyles";
function PedidosPage() {
  const { usuario } = useAuth();
  const [pedidos, setPedidos] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const fetchPedidos = async () => {
      if (!usuario) return;
      try {
        const res = await API.get(`/pedido/listar/${usuario.id}`);
        setPedidos(res.data);
      } catch (err) {
        console.error("Error cargando pedidos", err);
      }
      setLoading(false);
    };
    fetchPedidos();
  }, [usuario]);
  if (!usuario) {
    return (
      <div className="p-6 text-center text-gray-700">
        Debes iniciar sesión para ver tus pedidos.
      </div>
    );
  }
  if (loading) {
    return <div className="p-6 text-center">Cargando pedidos...</div>;
  }
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-green-700 mb-4">Mis pedidos</h1>
      {pedidos.length === 0 ? (
        <p className="text-gray-600">Aún no tienes pedidos.</p>
      ) : (
        <div className="space-y-4">
          {pedidos.map((pedido) => (
            <Link
              to={`/pedido/${pedido.id}`}
              key={pedido.id}
              className="block border rounded-lg p-4 hover:shadow-md transition"
            >
              <div className="flex justify-between items-center">
                <p className="font-semibold">Pedido #{pedido.id}</p>
                <span
                  className={`px-2 py-1 text-xs font-semibold rounded border ${
                    ESTADO_COLORES[pedido.estado] ||
                    "bg-gray-100 text-gray-700 border-gray-300"
                  }`}
                >
                  {pedido.estado.replace(/_/g, " ")}
                </span>
              </div>
              <p className="text-gray-700 text-sm mt-1">
                Total: <strong>S/ {pedido.total}</strong>
              </p>
              <p className="text-gray-500 text-xs mt-1">
                Fecha: {new Date(pedido.fecha).toLocaleDateString()}
              </p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
export default PedidosPage;
