import React from "react";
import { Truck, RefreshCcw, MapPin, Info } from "lucide-react";

export default function ProductPolicies() {
  return (
    <section className="text-gray-800">
      <h2 className="text-lg font-semibold mb-4">Políticas de envíos y devoluciones</h2>

      <ul className="space-y-3 text-sm">
        <li className="flex items-start gap-3">
          <Truck className="text-gray-700 mt-0.5 flex-shrink-0" size={18} />
          <span>
            Pídelo hoy para recibirlo en torno al{" "}
            <strong>30 oct - 5 nov</strong>
          </span>
        </li>
        <li className="flex items-start gap-3">
          <RefreshCcw className="text-gray-700 mt-0.5 flex-shrink-0" size={18} />
          <span>
            Se aceptan <strong>cambios y devoluciones</strong> en el plazo de 30 días
          </span>
        </li>
        <li className="flex items-start gap-3">
          <Truck className="text-gray-700 mt-0.5 flex-shrink-0" size={18} />
          <span>
            Gastos de envío: <strong>USD 16.70</strong>
          </span>
        </li>
        <li className="flex items-start gap-3">
          <MapPin className="text-gray-700 mt-0.5 flex-shrink-0" size={18} />
          <span>
            Se envía desde: <strong>Arequipa</strong> <br />
            Se envía a <strong>Arequipa</strong>
          </span>
        </li>
      </ul>

      {/* 🩵 ¿Lo sabías? */}
      <div className="mt-8 border-t pt-4 space-y-3">
        <h3 className="font-semibold text-gray-900 flex items-center gap-2">
          <Info className="text-gray-600" size={18} />
          ¿Lo sabías?
        </h3>
        <div className="text-sm text-gray-700 space-y-2">
          <p>
            <strong>Protección de compras</strong> — Compra con confianza sabiendo
            que estamos a tu lado si surge un problema con un pedido que reúne
            los requisitos.
          </p>
          <p className="bg-blue-50 p-3 rounded-md text-gray-800 border border-blue-100">
            Compensamos las emisiones de carbono de los envíos y embalajes de esta compra.
          </p>
        </div>
      </div>
    </section>
  );
}
