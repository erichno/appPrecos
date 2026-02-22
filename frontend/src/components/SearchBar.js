import React, { useState } from 'react';
import { Search, MapPin } from 'lucide-react';
import { productsAPI } from '../services/api';
import { useApp } from '../context/AppContext';

const SearchBar = ({ onSearch, autoFocus = false }) => {
  const { selectedCity } = useApp();
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);

  const handleInputChange = async (e) => {
    const value = e.target.value;
    setQuery(value);

    if (value.length >= 3 && selectedCity) {
      setLoading(true);
      try {
        const response = await productsAPI.search(value, selectedCity.id);
        setSuggestions(response.data);
        setShowSuggestions(true);
      } catch (error) {
        console.error('Search error:', error);
      } finally {
        setLoading(false);
      }
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim() && selectedCity) {
      setShowSuggestions(false);
      onSearch(query);
    }
  };

  const handleSuggestionClick = (product) => {
    setQuery(product.display_name);
    setShowSuggestions(false);
    onSearch(product.display_name, product);
  };

  return (
    <div className="relative w-full">
      <form onSubmit={handleSearch}>
        <div className="relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            value={query}
            onChange={handleInputChange}
            onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
            placeholder="Ex: leite integral 1L, arroz 5kg..."
            autoFocus={autoFocus}
            className="w-full pl-12 pr-4 py-4 text-lg border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
            data-testid="search-input"
          />
          {!selectedCity && (
            <div className="absolute right-4 top-1/2 transform -translate-y-1/2 flex items-center gap-2 text-amber-600">
              <MapPin className="w-5 h-5" />
              <span className="text-sm font-medium">Selecione uma cidade</span>
            </div>
          )}
        </div>
      </form>

      {/* Suggestions dropdown */}
      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute z-50 w-full mt-2 bg-white border border-gray-200 rounded-xl shadow-lg max-h-96 overflow-y-auto">
          {suggestions.map((product) => (
            <div
              key={product.id}
              onClick={() => handleSuggestionClick(product)}
              className="p-4 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0 flex items-center gap-4"
              data-testid={`suggestion-${product.id}`}
            >
              {product.image_url && (
                <img src={product.image_url} alt={product.display_name} className="w-12 h-12 object-cover rounded" />
              )}
              <div className="flex-1">
                <p className="font-medium text-gray-900">{product.display_name}</p>
                <p className="text-sm text-gray-500">{product.category}</p>
              </div>
              {product.best_offer && (
                <div className="text-right">
                  <p className="text-lg font-bold text-green-600">R$ {product.best_offer.price.toFixed(2)}</p>
                  <p className="text-xs text-gray-500">{product.best_offer.supermarket.name}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {loading && (
        <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
        </div>
      )}
    </div>
  );
};

export default SearchBar;
