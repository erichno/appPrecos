import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, TrendingDown, Heart, Bell } from 'lucide-react';
import SearchBar from '../components/SearchBar';
import { useApp } from '../context/AppContext';
import { useAuth } from '../context/AuthContext';
import { citiesAPI, usersAPI } from '../services/api';
import ProductCard from '../components/ProductCard';

const Home = () => {
  const navigate = useNavigate();
  const { selectedCity, setSelectedCity } = useApp();
  const { isAuthenticated } = useAuth();
  const [showCityModal, setShowCityModal] = useState(!selectedCity);
  const [cities, setCities] = useState([]);
  const [favorites, setFavorites] = useState({ products: [], supermarkets: [] });

  useEffect(() => {
    loadCities();
    if (isAuthenticated) {
      loadFavorites();
    }
  }, [isAuthenticated]);

  const loadCities = async () => {
    try {
      const response = await citiesAPI.getAll();
      setCities(response.data);
    } catch (error) {
      console.error('Failed to load cities:', error);
    }
  };

  const loadFavorites = async () => {
    try {
      const response = await usersAPI.getFavorites();
      setFavorites(response.data);
    } catch (error) {
      console.error('Failed to load favorites:', error);
    }
  };

  const handleCitySelect = (city) => {
    setSelectedCity(city);
    setShowCityModal(false);
  };

  const handleSearch = (query, product = null) => {
    if (product) {
      navigate(`/product/${product.id}`);
    } else {
      navigate(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <TrendingDown className="w-6 h-6 text-white" />
              </div>
              <h1 className="text-2xl font-bold text-gray-900">MelhorPreço</h1>
            </div>
            <div className="flex items-center gap-4">
              {selectedCity && (
                <button
                  onClick={() => setShowCityModal(true)}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-800 rounded-lg hover:bg-blue-200 transition-colors"
                  data-testid="change-city-button"
                >
                  <MapPin className="w-4 h-4" />
                  <span className="font-medium">{selectedCity.name}</span>
                </button>
              )}
              {isAuthenticated ? (
                <div className="flex gap-2">
                  <button
                    onClick={() => navigate('/favorites')}
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                    data-testid="favorites-button"
                  >
                    <Heart className="w-6 h-6 text-gray-600" />
                  </button>
                  <button
                    onClick={() => navigate('/alerts')}
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                    data-testid="alerts-button"
                  >
                    <Bell className="w-6 h-6 text-gray-600" />
                  </button>
                  <button
                    onClick={() => navigate('/profile')}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                    data-testid="profile-button"
                  >
                    Perfil
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => navigate('/auth')}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                  data-testid="login-button"
                >
                  Entrar
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h2 className="text-5xl font-bold text-gray-900 mb-4">
            Encontre os <span className="text-blue-600">melhores preços</span> da sua cidade
          </h2>
          <p className="text-xl text-gray-600">Compare supermercados em segundos e economize dinheiro</p>
        </div>

        <div className="max-w-3xl mx-auto mb-12">
          <SearchBar onSearch={handleSearch} autoFocus />
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white p-6 rounded-xl shadow-sm text-center">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <TrendingDown className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="font-bold text-lg mb-2">Preços Atualizados</h3>
            <p className="text-gray-600">Informações em tempo real de vários supermercados</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm text-center">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <MapPin className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="font-bold text-lg mb-2">Mercados Próximos</h3>
            <p className="text-gray-600">Encontre as melhores ofertas perto de você</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm text-center">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Bell className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="font-bold text-lg mb-2">Alertas de Preço</h3>
            <p className="text-gray-600">Receba notificações quando o preço baixar</p>
          </div>
        </div>

        {/* Favorites Section */}
        {isAuthenticated && favorites.products.length > 0 && (
          <div className="mt-16">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Seus Favoritos</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {favorites.products.slice(0, 3).map((product) => (
                <ProductCard key={product.id} product={product} compact />
              ))}
            </div>
          </div>
        )}
      </div>

      {/* City Selection Modal */}
      {showCityModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Selecione sua cidade</h2>
            <p className="text-gray-600 mb-6">Escolha a cidade para ver os preços dos supermercados locais</p>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {cities.map((city) => (
                <button
                  key={city.id}
                  onClick={() => handleCitySelect(city)}
                  className="w-full text-left px-4 py-3 hover:bg-blue-50 rounded-lg transition-colors border border-gray-200"
                  data-testid={`city-option-${city.id}`}
                >
                  <div className="font-semibold text-gray-900">{city.name}</div>
                  <div className="text-sm text-gray-500">{city.state}</div>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
