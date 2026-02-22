import React from 'react';
import { MapPin, Phone, Clock, Star } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const SupermarketCard = ({ supermarket, showDistance = true }) => {
  const navigate = useNavigate();

  return (
    <div
      onClick={() => navigate(`/supermarket/${supermarket.id}`)}
      className="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-shadow cursor-pointer"
      data-testid={`supermarket-card-${supermarket.id}`}
    >
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-bold text-gray-900">{supermarket.name}</h3>
          {supermarket.chain && (
            <p className="text-sm text-gray-500 mt-1">{supermarket.chain}</p>
          )}
        </div>
        <div className="flex items-center gap-1">
          <Star className="w-5 h-5 text-yellow-400 fill-current" />
          <span className="font-semibold">{supermarket.rating.toFixed(1)}</span>
          <span className="text-sm text-gray-500">({supermarket.total_reviews})</span>
        </div>
      </div>

      <div className="space-y-2 text-sm text-gray-600">
        <div className="flex items-start gap-2">
          <MapPin className="w-4 h-4 mt-0.5 flex-shrink-0" />
          <span>
            {supermarket.address.street}, {supermarket.address.neighborhood}
          </span>
        </div>

        {supermarket.contact?.phone && (
          <div className="flex items-center gap-2">
            <Phone className="w-4 h-4" />
            <span>{supermarket.contact.phone}</span>
          </div>
        )}

        {supermarket.opening_hours && (
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4" />
            <span>Aberto hoje: {supermarket.opening_hours.monday || 'Consultar horário'}</span>
          </div>
        )}

        {showDistance && supermarket.distance_km !== undefined && (
          <div className="mt-3 inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full font-medium">
            {supermarket.distance_km.toFixed(1)} km de distância
          </div>
        )}
      </div>
    </div>
  );
};

export default SupermarketCard;
