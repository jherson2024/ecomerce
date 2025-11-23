// src/app/App.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "../pages/HomePage";
import ProductDetail from "../pages/ProductDetail";
import Navbar from "../components/Navbar";
import { SearchProvider } from "../context/SearchContext";
import "./index.css";
import StoreDetail from "../pages/StoreDetail";
import CollectionDetail from "../pages/CollectionDetail";
import CarritoPage from "../pages/CarritoPage"; // 👈 AÑADIDO
import CheckoutPage from "../pages/CheckoutPage";
import PedidoDetailPage from "../pages/PedidoDetailPage";
import PedidosPage from "../pages/PedidosPage";
function App() {
  return (
    <BrowserRouter>
      <SearchProvider>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/producto/:producto_id" element={<ProductDetail />} />
          <Route path="/tienda/:vendedor_id" element={<StoreDetail />} />
          <Route
            path="/tienda/:vendedor_id/coleccion/:coleccion_id"
            element={<CollectionDetail />}
          />
          <Route path="/carrito" element={<CarritoPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
          <Route path="/pedido/:pedido_id" element={<PedidoDetailPage />} />
          <Route path="/pedidos" element={<PedidosPage />} />
        </Routes>
      </SearchProvider>
    </BrowserRouter>
  );
}
export default App;
