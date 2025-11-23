import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import API from "../api/axios";
import { ArrowLeft } from "lucide-react";
import ProductTopBar from "./ProductTopBar";
import ProductGallery from "./ProductGallery";
import ProductInfo from "./ProductInfo";
import ProductPolicies from "./ProductPolicies";
import ProductReviews from "./ProductReviews";
import StoreSection from "./StoreSection";
import SimilarProducts from "./SimilarProducts";

export default function ProductDetail() {
  const { producto_id } = useParams();
  const [producto, setProducto] = useState(null);
  const [loading, setLoading] = useState(true);
  const [imagenIndex, setImagenIndex] = useState(0);

  useEffect(() => {
    const fetchDetalle = async () => {
      try {
        const res = await API.get(`/producto/detalle/${producto_id}`);
        setProducto(res.data);
      } catch {
        console.error("Error al cargar el producto");
      } finally {
        setLoading(false);
      }
    };
    fetchDetalle();
  }, [producto_id]);

  if (loading) return <p className="text-center mt-10 animate-pulse">Cargando...</p>;
  if (!producto) return <p className="text-center mt-10">Producto no encontrado.</p>;

  const imagenes = [producto.imagen, ...producto.opciones.filter(o => o.imagen).map(o => o.imagen)].filter(Boolean);
  const cambiarImagen = (dir) =>
    setImagenIndex((prev) =>
      dir === "next" ? (prev + 1) % imagenes.length : (prev - 1 + imagenes.length) % imagenes.length
    );

  return (
    <div className="max-w-7xl mx-auto px-6 py-0">

      <ProductTopBar />
      <SimilarProducts productos={producto.productos_similares} />

      <div className="grid lg:grid-cols-2 gap-12 bg-white border-t-1 rounded-2xl p-0 -mt-4 pt-3 pl-3">
        <ProductGallery
          imagenes={imagenes}
          imagenIndex={imagenIndex}
          cambiarImagen={cambiarImagen}
          setImagenIndex={setImagenIndex}
          nombre={producto.nombre}
        />
        <ProductInfo producto={producto} />
      </div>

      <div className="grid md:grid-cols-2 gap-8 mt-10">
        <ProductReviews reseñas={producto.reseñas} />
        <ProductPolicies />
      </div>

      <StoreSection tienda={producto.tienda} />
    </div>
  );
}
