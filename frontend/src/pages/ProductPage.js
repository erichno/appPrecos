import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Heart, Bell, MapPin, TrendingDown, Clock } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { productsAPI, offersAPI, usersAPI } from '../services/api';
import { useApp } from '../context/AppContext';
import { useAuth } from '../context/AuthContext';
import { toast } from 'sonner';

const ProductPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { selectedCity } = useApp();
  const { isAuthenticated } = useAuth();
  const [product, setProduct] = useState(null);
  const [offers, setOffers] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isFavorite, setIsFavorite] = useState(false);

  useEffect(() => {
    if (selectedCity) {
      loadProduct();
      loadOffers();
      loadHistory();
    }
  }, [id, selectedCity]);

  const loadProduct = async () => {
    try {
      const response = await productsAPI.getById(id);
      setProduct(response.data);
    } catch (error) {
      console.error('Failed to load product:', error);
      toast.error('Erro ao carregar produto');
    }
  };

  const loadOffers = async () => {
    try {
      const response = await offersAPI.getOffers(id, selectedCity.id);
      setOffers(response.data);
    } catch (error) {
      console.error('Failed to load offers:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadHistory = async () => {
    try {
      const response = await productsAPI.getHistory(id, selectedCity.id, 30);
      // Transform data for chart
      const chartData = response.data.history.reduce((acc, item) => {
        const date = new Date(item.date).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
        const existing = acc.find((d) => d.date === date);
        if (existing) {
          existing[item.supermarket_name] = item.price;
        } else {
          acc.push({ date, [item.supermarket_name]: item.price });
        }
        return acc;
      }, []);
      setHistory(chartData);
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  };

  const toggleFavorite = async () => {
    if (!isAuthenticated) {
      toast.error('Você precisa estar logado');
      navigate('/auth');
      return;
    }

    try {
      if (isFavorite) {
        await usersAPI.removeFavorite('product', id);
        setIsFavorite(false);
        toast.success('Removido dos favoritos');
      } else {
        await usersAPI.addFavorite('product', id);
        setIsFavorite(true);
        toast.success('Adicionado aos favoritos');
      }
    } catch (error) {
      toast.error('Erro ao atualizar favoritos');
    }
  };

  const createAlert = () => {
    if (!isAuthenticated) {
      toast.error('Você precisa estar logado');
      navigate('/auth');
      return;
    }
    navigate(`/alerts/create?product_id=${id}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-xl text-gray-600">Produto não encontrado</p>
      </div>
    );
  }

  const bestOffer = offers[0];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate(-1)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              data-testid="back-button"
            >
              <ArrowLeft className="w-6 h-6" />
            </button>
            <div className="flex gap-2">
              <button
                onClick={toggleFavorite}
                className={`p-2 rounded-lg transition-colors ${
                  isFavorite ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
                data-testid="favorite-button"
              >
                <Heart className={`w-6 h-6 ${isFavorite ? 'fill-current' : ''}`} />
              </button>
              <button
                onClick={createAlert}
                className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
                data-testid="alert-button"
              >
                <Bell className="w-6 h-6" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Product Info */}
        <div className="bg-white rounded-xl p-8 mb-6">
          <div className="flex gap-8">
            {product.image_url && (
              <img src={product.image_url} alt={product.display_name} className="w-64 h-64 object-cover rounded-lg" />
            )}
            <div className="flex-1">
              <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full mb-3">
                {product.category}
              </span>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">{product.display_name}</h1>
              <p className="text-xl text-gray-600 mb-6">
                {product.brand} • {product.size}
              </p>

              {bestOffer && (
                <div className="bg-green-50 border-2 border-green-200 rounded-xl p-6">
                  <p className="text-sm text-gray-600 mb-2">🏆 MELHOR PREÇO</p>
                  <p className="text-5xl font-bold text-green-600 mb-4">R$ {bestOffer.price.toFixed(2)}</p>
                  <div className="flex items-center gap-4 text-gray-700">
                    <div className="flex items-center gap-2">
                      <MapPin className="w-5 h-5" />
                      <span className="font-semibold">{bestOffer.supermarket?.name}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="w-5 h-5" />
                      <span>Atualizado há {bestOffer.hours_ago}h</span>
                    </div>
                  </div>
                  {bestOffer.is_promotion && (
                    <div className="mt-3">
                      <span className="px-3 py-1 bg-red-500 text-white text-sm font-semibold rounded-full">
                        🔥 EM PROMOÇÃO
                      </span>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Price History Chart */}
        {history.length > 0 && (
          <div className="bg-white rounded-xl p-8 mb-6">
            <div className="flex items-center gap-2 mb-6">
              <TrendingDown className="w-6 h-6 text-blue-600" />
              <h2 className="text-2xl font-bold text-gray-900">Histórico de Preços (30 dias)</h2>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip formatter={(value) => `R$ ${value.toFixed(2)}`} />
                <Legend />
                {Object.keys(history[0] || {})
                  .filter((key) => key !== 'date')
                  .map((supermarket, index) => (
                    <Line
                      key={supermarket}
                      type="monotone"
                      dataKey={supermarket}
                      stroke={['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'][index % 5]}
                      strokeWidth={2}
                    />
                  ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* All Offers */}
        <div className="bg-white rounded-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Onde comprar</h2>
          <div className="space-y-4">
            {offers.map((offer, index) => (
              <div
                key={offer.id}
                className={`p-6 rounded-lg border-2 ${
                  index === 0 ? 'border-green-500 bg-green-50' : 'border-gray-200'
                }`}
                data-testid={`offer-${offer.id}`}
              >
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{offer.supermarket?.name}</h3>
                    <p className="text-gray-600">{offer.supermarket?.address?.neighborhood}</p>
                    <p className="text-sm text-gray-500 mt-2">Atualizado há {offer.hours_ago}h</p>
                  </div>
                  <div className="text-right">
                    <p className={`text-3xl font-bold ${index === 0 ? 'text-green-600' : 'text-gray-900'}`}>
                      R$ {offer.price.toFixed(2)}
                    </p>
                    {offer.is_promotion && (
                      <span className="inline-block mt-2 px-3 py-1 bg-red-500 text-white text-xs font-semibold rounded-full">
                        PROMOÇÃO
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {offers.length === 0 && (
            <p className="text-center text-gray-500 py-8">Nenhuma oferta disponível no momento</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductPage;
