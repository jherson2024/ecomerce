import React from "react";
import { ShieldCheck, CreditCard, BadgeCheck, Star } from "lucide-react";

const infoItems = [
  { icon: ShieldCheck, title: "Compra con confianza", desc: "Tu compra está protegida si surge algún problema." },
  { icon: ShieldCheck, title: "Protección de compras", desc: "Te ayudamos si algo sale mal con tu pedido." },
  { icon: CreditCard, title: "Opciones de pago seguras", desc: "Pagos protegidos y cifrados de extremo a extremo." },
  { icon: Star, title: "Reseñas verificadas", desc: "Opiniones reales de compradores confirmados." },
];

export default function ProductTopBar() {
  return (
    <div className="w-full bg-gray-100 border-y py-3 flex flex-wrap justify-center gap-10 text-sm text-gray-700">
      {infoItems.map((item, i) => (
        <div
          key={i}
          className="relative flex items-center gap-2 cursor-pointer group hover:text-gray-900 transition"
        >
          <item.icon size={18} className="text-green-700" />
          <span className="font-medium">{item.title}</span>
          <div className="absolute top-full mt-2 w-64 bg-white text-gray-600 text-xs p-3 rounded-md shadow-lg border opacity-0 group-hover:opacity-100 transition pointer-events-none z-20">
            {item.desc}
          </div>
        </div>
      ))}
    </div>
  );
}
