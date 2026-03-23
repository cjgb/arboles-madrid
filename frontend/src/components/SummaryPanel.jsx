import React from 'react';

const SummaryPanel = ({ loading, error, summary }) => {
  if (!loading && !error && !summary) return null;

  return (
    <div className="absolute bottom-6 left-6 z-[1000] max-w-sm w-full bg-white rounded-lg shadow-lg p-6 border border-gray-100">
      {loading && (
        <div className="flex items-center space-x-3">
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
          <p className="text-gray-600 font-medium">Calculando ruta...</p>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4">
          <p className="text-sm text-red-700 font-medium">Error: {error}</p>
        </div>
      )}

      {!loading && summary && (
        <div className="space-y-4">
          <div className="border-b pb-3 border-gray-100">
            <div className="text-center">
              <p className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Distancia Total</p>
              <p className="text-lg font-bold text-gray-800">{summary.distance_km.toFixed(1)} <span className="text-xs font-normal">km</span></p>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between items-center text-xs">
              <span className="text-gray-500 font-medium">🛣️ Distancia por calles:</span>
              <span className="text-gray-700 font-bold">{summary.road_distance_km.toFixed(2)} km</span>
            </div>
            <div className="flex justify-between items-center text-xs">
              <span className="text-green-600 font-medium">🌳 Distancia por arbolado:</span>
              <span className="text-green-700 font-bold">{summary.tree_distance_km.toFixed(2)} km</span>
            </div>
            <div className="flex justify-between items-center text-xs">
              <span className="text-green-600 font-medium">🦜 Número de saltos entre árboles:</span>
              <span className="text-green-700 font-bold">{summary.tree_hops}</span>
            </div>

            {/* Progress bar for Tree coverage */}
            <div className="w-full bg-gray-100 rounded-full h-1.5 mt-2">
              <div
                className="bg-green-500 h-1.5 rounded-full"
                style={{ width: `${(summary.tree_distance_km / summary.distance_km) * 100}%` }}
              ></div>
            </div>
          </div>

          {/*
          <div className="pt-2">
            <p className="text-xs leading-relaxed text-gray-500 italic">
              "{summary.summary}"
            </p>
          </div>
          */}
        </div>
      )}
    </div>
  );
};

export default SummaryPanel;
