// src/context/SearchContext.jsx
import React, { createContext, useContext, useState } from "react";

const SearchContext = createContext();

export const SearchProvider = ({ children }) => {
  const [searchQuery, setSearchQuery] = useState(null);
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState(null);

  return (
    <SearchContext.Provider
      value={{
        searchQuery,
        setSearchQuery,
        categoriaSeleccionada,
        setCategoriaSeleccionada,
      }}
    >
      {children}
    </SearchContext.Provider>
  );
};

export const useSearch = () => useContext(SearchContext);
