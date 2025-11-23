import React, { useState } from "react";
import API from "../api/axios";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function CheckoutPage() {
  const { usuario } = useAuth();
  const navigate = useNavigate();

  const [direccion, setDireccion] = useState("");
  const [distritoId, setDistritoId] = useState("");
  const [loading, setLoading] = useState(false);

  const [qrData, setQrData] = useState(null); // contiene url_pago, qr_imagen, pedido_id

  const procesarPago = async () => {
    if (!direccion || !distritoId) {
      alert("Completa todos los campos.");
      return;
    }

    try {
      setLoading(true);

      const body = {
        usuario_id: usuario.id,
        metodopago_id: 1, // SOLO QR
        distrito_id: Number(distritoId),
        direccion: direccion,
        referencia: ""
      };

      const res = await API.post("/checkout/procesar", body);

      // Guardar respuesta con pedido_id
      setQrData({
        pedido_id: res.data.pedido_id,   // ← NUEVO
        url_pago: res.data.url_pago,
        qr_imagen: res.data.qr_imagen,
      });

    } catch (err) {
      console.error("ERROR BACKEND:", err.response?.data);
      alert("Error al procesar pago: " + JSON.stringify(err.response?.data));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-4">Checkout</h1>

      <div className="space-y-4">
        {/* DIRECCIÓN */}
        <div>
          <label className="block text-sm font-medium">Dirección de entrega</label>
          <input
            className="border rounded-lg w-full px-3 py-2"
            value={direccion}
            onChange={(e) => setDireccion(e.target.value)}
          />
        </div>

        {/* DISTRITO */}
        <div>
          <label className="block text-sm font-medium">Distrito</label>
          <select
            className="border rounded-lg w-full px-3 py-2"
            value={distritoId}
            onChange={(e) => setDistritoId(e.target.value)}
          >
            <option value="">Selecciona un distrito</option>
            <option value="1">Cercado</option>
            <option value="2">Otro distrito</option>
          </select>
        </div>

        {/* MÉTODO DE PAGO */}
        <div>
          <label className="block text-sm font-medium">Método de pago</label>
          <select className="border rounded-lg w-full px-3 py-2" disabled>
            <option value="1">Yape / Plin (QR)</option>
          </select>
        </div>

        {/* BOTÓN */}
        <button
          onClick={procesarPago}
          className="w-full bg-green-700 text-white py-3 rounded-lg mt-4 hover:bg-green-800"
          disabled={loading}
        >
          {loading ? "Procesando..." : "Generar QR de pago"}
        </button>
      </div>

      {/* MODAL QR */}
      {qrData && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-[99999]">
          <div className="bg-white p-6 rounded-xl shadow-lg text-center max-w-sm">
            <h2 className="text-xl font-semibold mb-4">Pagar con Yape / Plin</h2>

            <img
              src={qrData.qr_imagen}
              alt="QR de pago"
              className="w-64 h-64 object-cover mx-auto mb-4 border rounded-lg"
            />

            <p className="text-sm text-gray-700 mb-3">
              Escanea este código QR con Yape o Plin para completar tu pago.
            </p>

            <a
              href={qrData.url_pago}
              target="_blank"
              className="text-blue-600 underline block mb-4"
            >
              Abrir enlace de pago
            </a>

            <button
              onClick={() => navigate(`/pedido/${qrData.pedido_id}`)} // ← REDIRECCIÓN AQUÍ
              className="bg-gray-300 px-4 py-2 rounded-lg hover:bg-gray-400"
            >
              Ver detalle del pedido
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
