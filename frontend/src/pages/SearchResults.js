import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Filter } from 'lucide-react';
import { productsAPI } from '../services/api';
import { useApp } from '../context/AppContext';
import ProductCard from '../components/ProductCard';
import SearchBar from '../components/SearchBar';

const SearchResults = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { selectedCity } = useApp();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const query = searchParams.get('q');

  useEffect(() => {
    if (query && selectedCity) {
      searchProducts(query);
    }
  }, [query, selectedCity]);

  const searchProducts = async (q) => {
    setLoading(true);
    try {
      const response = await productsAPI.search(q, selectedCity.id);
      setProducts(response.data);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleNewSearch = (newQuery) => {
    navigate(`/search?q=${encodeURIComponent(newQuery)}`);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-4 mb-4">
            <button
              onClick={() => navigate('/')}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              data-testid="back-button"
            >
              <ArrowLeft className="w-6 h-6" />
            </button>
            <div className="flex-1">
              <SearchBar onSearch={handleNewSearch} />
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Results Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Resultados para "{query}"
          </h1>
          <p className="text-gray-600">
            {loading ? 'Buscando...' : `${products.length} produto(s) encontrado(s)`}
          </p>
        </div>

        {/* Loading */}
        {loading && (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        )}

        {/* No Results */}
        {!loading && products.length === 0 && (
          <div className="text-center py-20">
            <p className="text-xl text-gray-600 mb-4">Nenhum produto encontrado</p>
            <p className="text-gray-500">Tente buscar por outro termo</p>
          </div>
        )}

        {/* Results */}
        {!loading && products.length > 0 && (
          <div className="space-y-4" data-testid="search-results">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchResults;
