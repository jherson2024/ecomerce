// src/layout/MainLayout.jsx
import React from "react";
import Navbar from "../components/Navbar";

function MainLayout({ children, onCategoriaSelect, onSearch }) {
  return (
    <div className="bg-neutral-50 min-h-screen">
      <Navbar onCategoriaSelect={onCategoriaSelect} onSearch={onSearch} />
      <main className="max-w-7xl mx-auto px-6 py-10">{children}</main>
    </div>
  );
}

export default MainLayout;
