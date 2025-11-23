import React from "react";

/**
 * Botón reutilizable con variantes y clases dinámicas.
 * 
 * @param {string} variant - Tipo de botón ("default", "outline", "destructive", "ghost")
 * @param {boolean} disabled - Deshabilita el botón
 * @param {string} className - Clases extra
 * @param {function} onClick - Acción al hacer clic
 * @param {React.ReactNode} children - Contenido dentro del botón
 */
export function Button({
  children,
  onClick,
  variant = "default",
  disabled = false,
  className = "",
  type = "button",
}) {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-lg font-medium transition duration-150 focus:outline-none focus:ring-2 focus:ring-offset-1 text-sm px-3 py-2";

  const variants = {
    default:
      "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-400 disabled:bg-blue-300",
    outline:
      "border border-gray-300 bg-white text-gray-700 hover:bg-gray-100 focus:ring-gray-300 disabled:opacity-60",
    destructive:
      "bg-red-600 text-white hover:bg-red-700 focus:ring-red-400 disabled:bg-red-300",
    ghost:
      "text-gray-700 hover:bg-gray-100 focus:ring-gray-300 disabled:opacity-60",
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${base} ${variants[variant]} ${className}`}
    >
      {children}
    </button>
  );
}
