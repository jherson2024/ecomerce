import React, { useEffect, useState } from "react";
import API from "../api/axios";
import { Trash2, Plus, Minus, Loader2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { Link, useNavigate } from "react-router-dom";

export default function CarritoPage() {
  const { usuario } = useAuth();
  const navigate = useNavigate();
  const [carrito, setCarrito] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!usuario) return;
    fetchCarrito();
  }, [usuario]);

  const fetchCarrito = async () => {
    setLoading(true);
    try {
      const res = await API.get(`/carrito/obtener/${usuario.id}`);
      setCarrito(res.data);
    } finally {
      setLoading(false);
    }
  };

  const actualizarCantidad = async (detalleId, nuevaCantidad) => {
    if (nuevaCantidad < 1) return;

    setCarrito(prev => ({
      ...prev,
      detalles: prev.detalles.map(d =>
        d.id === detalleId
          ? { ...d, cantidad: nuevaCantidad, subtotal: d.precio * nuevaCantidad }
          : d
      ),
      total: prev.detalles.reduce((sum, d) =>
        sum + (d.id === detalleId ? d.precio * nuevaCantidad : d.subtotal), 0)
    }));

    try {
      await API.put(`/carrito/actualizar/${detalleId}?cantidad=${nuevaCantidad}`);
    } catch {
      fetchCarrito();
    }
  };

  const eliminarProducto = async (detalleId) => {
    try {
      await API.delete(`/carrito/eliminar/${detalleId}`);
      await fetchCarrito();
    } catch {}
  };

  const vaciarCarrito = async () => {
    if (!window.confirm("¿Deseas vaciar el carrito?")) return;
    try {
      await API.delete(`/carrito/vaciar/${usuario.id}`);
      await fetchCarrito();
    } catch {}
  };

  if (!usuario)
    return (
      <div className="text-center mt-20">
        <p className="text-xl">Debes iniciar sesión para ver tu carrito.</p>
        <Link to="/" className="text-green-700 underline mt-4 block">
          Volver al inicio
        </Link>
      </div>
    );

  if (loading)
    return (
      <div className="flex justify-center mt-20">
        <Loader2 size={32} className="animate-spin text-green-700" />
      </div>
    );

  if (!carrito || carrito.detalles.length === 0)
    return (
      <div className="text-center mt-20">
        <h2 className="text-2xl font-semibold mb-2">Tu carrito está vacío</h2>
        <Link
          to="/"
          className="bg-green-700 text-white px-6 py-3 rounded-full hover:bg-green-800"
        >
          Ver productos
        </Link>
      </div>
    );

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-semibold mb-6">Tu carrito</h1>

      <div className="space-y-6">
        {carrito.detalles.map((item) => (
          <div key={item.id} className="flex items-center bg-white shadow-sm border rounded-xl p-4">
            <img src={item.imagen} alt={item.nombre} className="w-20 h-20 object-cover rounded-lg border" />

            <div className="ml-4 flex-grow">
              <h3 className="font-semibold">{item.nombre}</h3>
              <p className="text-green-700 font-medium text-lg">S/ {item.precio.toFixed(2)}</p>

              <div className="flex items-center mt-2 gap-2">
                <button
                  onClick={() => actualizarCantidad(item.id, item.cantidad - 1)}
                  className="p-1 bg-gray-200 rounded-full hover:bg-gray-300"
                >
                  <Minus size={16} />
                </button>

                <input
                  type="number"
                  min="1"
                  className="w-16 text-center border rounded-lg"
                  value={item.cantidad}
                  onChange={(e) => {
                    const val = Number(e.target.value);
                    if (val > 0) actualizarCantidad(item.id, val);
                  }}
                />

                <button
                  onClick={() => actualizarCantidad(item.id, item.cantidad + 1)}
                  className="p-1 bg-gray-200 rounded-full hover:bg-gray-300"
                >
                  <Plus size={16} />
                </button>
              </div>
            </div>

            <div className="text-right">
              <p className="font-semibold">S/ {item.subtotal.toFixed(2)}</p>

              <button
                onClick={() => eliminarProducto(item.id)}
                className="mt-2 text-red-600 hover:text-red-800 flex items-center gap-1"
              >
                <Trash2 size={18} /> Eliminar
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* RESUMEN */}
      <div className="mt-8 p-6 bg-white rounded-xl shadow-sm border">
        <div className="flex justify-between text-lg font-medium mb-4">
          <span>Total:</span>
          <span className="text-green-700 font-bold">S/ {carrito.total.toFixed(2)}</span>
        </div>

        <button
          onClick={vaciarCarrito}
          className="text-red-600 underline text-sm mb-4"
        >
          Vaciar carrito
        </button>

        <button
          onClick={() => navigate("/checkout")}
          className="w-full bg-green-700 text-white py-3 rounded-full hover:bg-green-800"
        >
          Ir al Checkout
        </button>
      </div>
    </div>
  );
}
