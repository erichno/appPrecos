import React from 'react';
import { Star, MapPin, Clock } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const ProductCard = ({ product, compact = false }) => {
  const navigate = useNavigate();
  const bestOffer = product.best_offer;

  if (compact) {
    return (
      <div
        onClick={() => navigate(`/product/${product.id}`)}
        className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
        data-testid={`product-card-${product.id}`}
      >
        <div className="flex gap-3">
          {product.image_url && (
            <img src={product.image_url} alt={product.display_name} className="w-16 h-16 object-cover rounded" />
          )}
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-gray-900 truncate">{product.display_name}</h3>
            <p className="text-sm text-gray-500">{product.brand}</p>
            {bestOffer && (
              <p className="text-lg font-bold text-green-600 mt-1">R$ {bestOffer.price.toFixed(2)}</p>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      onClick={() => navigate(`/product/${product.id}`)}
      className="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all cursor-pointer"
      data-testid={`product-card-${product.id}`}
    >
      <div className="flex gap-6">
        {product.image_url && (
          <img src={product.image_url} alt={product.display_name} className="w-32 h-32 object-cover rounded-lg" />
        )}
        <div className="flex-1">
          <div className="flex justify-between items-start mb-2">
            <div>
              <h3 className="text-xl font-bold text-gray-900">{product.display_name}</h3>
              <p className="text-gray-600 mt-1">
                {product.brand} • {product.size}
              </p>
              <span className="inline-block mt-2 px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                {product.category}
              </span>
            </div>
            {bestOffer && bestOffer.is_promotion && (
              <span className="px-3 py-1 bg-red-500 text-white text-sm font-semibold rounded-full">🔥 PROMOÇÃO</span>
            )}
          </div>

          {bestOffer && (
            <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex justify-between items-center">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Menor preço encontrado</p>
                  <p className="text-3xl font-bold text-green-600">R$ {bestOffer.price.toFixed(2)}</p>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-gray-900">{bestOffer.supermarket.name}</p>
                  <div className="flex items-center gap-1 text-sm text-gray-500 mt-1">
                    <MapPin className="w-4 h-4" />
                    <span>{bestOffer.supermarket.distance_km.toFixed(1)} km</span>
                  </div>
                  <div className="flex items-center gap-1 text-sm text-gray-500 mt-1">
                    <Clock className="w-4 h-4" />
                    <span>Atualizado há {bestOffer.hours_ago}h</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
