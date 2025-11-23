import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import API from "../api/axios";
import { ESTADO_COLORES } from "../utils/EstadoStyles";

export default function PedidoDetailPage() {
  const { pedido_id } = useParams();
  const [pedido, setPedido] = useState(null);
  const [loading, setLoading] = useState(true);

  const obtenerPedido = async () => {
    try {
      const res = await API.get(`/checkout/pedido/${pedido_id}`);
      setPedido(res.data);
    } catch (err) {
      console.error("Error cargando pedido", err);
      alert("No se pudo cargar el pedido");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    obtenerPedido();
  }, []);

  if (loading)
    return <div className="p-6 text-center text-lg">Cargando pedido...</div>;

  if (!pedido)
    return (
      <div className="p-6 text-center text-red-600">
        No se encontró el pedido.
      </div>
    );

  return (
    <div className="max-w-3xl mx-auto p-6 relative">

      {/* 🔥 Sello diagonal si NO está pagado */}
      {pedido.pago.estado === "PAGO_PENDIENTE" && (
        <div className="absolute top-10 right-10 rotate-12 text-red-600
                        text-4xl font-black opacity-20 pointer-events-none">
          NO PAGADO
        </div>
      )}

      <h1 className="text-2xl font-semibold mb-4">Detalle del Pedido</h1>

      {/* INFO PRINCIPAL */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <p><strong>ID Pedido:</strong> {pedido.pedido_id}</p>
        <p><strong>Fecha:</strong> {new Date(pedido.fecha).toLocaleString()}</p>
        <p><strong>Total:</strong> S/ {pedido.total}</p>

        {/* Estado con color */}
        <p className="flex items-center gap-2">
          <strong>Estado:</strong>
          <span className={`px-3 py-1 rounded-full border text-sm font-semibold 
            ${ESTADO_COLORES[pedido.estado] || "bg-gray-200 text-gray-700"}`}>
            {pedido.estado}
          </span>
        </p>

        <p><strong>Método de Pago:</strong> {pedido.metodopago}</p>
      </div>

      {/* DIRECCIÓN */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h2 className="text-lg font-semibold mb-2">Dirección de entrega</h2>
        <p><strong>Distrito:</strong> {pedido.distrito}</p>
        <p><strong>Dirección:</strong> {pedido.direccion}</p>
        {pedido.referencia && (
          <p><strong>Referencia:</strong> {pedido.referencia}</p>
        )}
      </div>

      {/* PRODUCTOS */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h2 className="text-lg font-semibold mb-4">Productos</h2>

        {pedido.productos.map((prod) => (
          <div key={prod.producto_id} className="flex gap-3 border-b py-3">
            <img
              src={prod.imagen}
              alt={prod.nombre}
              className="w-20 h-20 object-cover rounded-md border"
            />
            <div>
              <p className="font-semibold">{prod.nombre}</p>
              <p>Cantidad: {prod.cantidad}</p>
              <p>Precio: S/ {prod.precio}</p>
              <p>Subtotal: S/ {prod.subtotal}</p>
              {prod.opciones.length > 0 && (
                <div className="mt-1 text-sm text-gray-600">
                  <strong>Opciones:</strong>
                  {prod.opciones.map((op, idx) => (
                    <div key={idx}>
                      {op.nombre}: {op.valor}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      {/* PAGO */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h2 className="text-lg font-semibold mb-2">Pago</h2>
        <p className="flex items-center gap-2">
          <strong>Estado:</strong>
          <span className={`px-3 py-1 rounded-full border text-sm font-semibold
            ${ESTADO_COLORES[pedido.pago.estado] || "bg-gray-200 text-gray-700"}`}>
            {pedido.pago.estado}
          </span>
        </p>
        <p><strong>Monto:</strong> S/ {pedido.pago.monto}</p>
        {/* Enlace de pago si pendiente */}
        {pedido.pago.estado === "PAGO_PENDIENTE" && (
          <div className="mt-4">
            <a
              href={pedido.pago.url}
              target="_blank"
              className="bg-green-600 text-white px-4 py-2 rounded-lg"
            >
              Abrir enlace de pago
            </a>
          </div>
        )}
      </div>
      {/* ENVÍO */}
      {pedido.envio && (
        <div className="bg-white p-4 rounded-lg shadow mb-6">
          <h2 className="text-lg font-semibold mb-2">Envío</h2>
          <p className="flex items-center gap-2">
            <strong>Estado:</strong>
            <span className={`px-3 py-1 rounded-full border text-sm font-semibold
              ${ESTADO_COLORES[pedido.envio.estado] || "bg-gray-200 text-gray-700"}`}>
              {pedido.envio.estado}
            </span>
          </p>
          <p><strong>Transportista:</strong> {pedido.envio.transportista}</p>
          <p><strong>Código:</strong> {pedido.envio.codigo || "—"}</p>
          {pedido.envio.url && (
            <a
              href={pedido.envio.url}
              target="_blank"
              className="text-blue-600 underline mt-2 block"
            >
              Ver seguimiento
            </a>
          )}
        </div>
      )}
      {/* VENDEDOR */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h2 className="text-lg font-semibold mb-2">Vendedor</h2>
        <p><strong>Nombre:</strong> {pedido.vendedor.nombre}</p>
        {pedido.vendedor.logo && (
          <img
            src={pedido.vendedor.logo}
            className="w-24 h-24 rounded-md mt-2 border"
            alt="logo tienda"
          />
        )}
      </div>
      {/* BOTONES */}
      <div className="mt-8 flex justify-between">
        <Link
          to="/"
          className="px-4 py-2 bg-gray-300 rounded-lg hover:bg-gray-400"
        >
          Volver a inicio
        </Link>
      </div>
    </div>
  );
}