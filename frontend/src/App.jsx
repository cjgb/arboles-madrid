import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MapView from './components/MapView';
import SummaryPanel from './components/SummaryPanel';
import InfoModal from './components/InfoModal';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function App() {
  const [route, setRoute] = useState(null);
  const [treePoints, setTreePoints] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [summary, setSummary] = useState(null);
  
  // State for Step 8: Bells and Whistles
  const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);
  const [isFirstVisit, setIsFirstVisit] = useState(false);

  useEffect(() => {
    // Check if user has visited before
    const hasVisited = localStorage.getItem('hasVisitedMadridRouting');
    if (!hasVisited) {
      setIsFirstVisit(true);
      setIsInfoModalOpen(true);
      localStorage.setItem('hasVisitedMadridRouting', 'true');
    }
  }, []);

  const handlePointsSelected = async (start, end) => {
    setLoading(true);
    setError(null);
    setSummary(null);
    setRoute(null);
    setTreePoints(null);

    try {
      // 1. Fetch the route from the backend
      const routeResponse = await axios.post(`${API_BASE_URL}/route`, {
        start,
        end,
        profile: 'driving-car'
      });

      const feature = routeResponse.data.features[0];
      const coords = feature.geometry.coordinates;
      
      // Leaflet expects [lat, lon], ORS provides [lon, lat]
      const leafletCoords = coords.map(coord => [coord[1], coord[0]]);
      setRoute(leafletCoords);

      // Extract tree points
      const points = feature.properties.tree_points || [];
      setTreePoints(points);

      // 2. Extract stats (distance is in meters, duration in seconds)
      const segments = feature.properties.segments[0];
      const { distance, duration, tree_distance, road_distance, tree_hops } = segments;
      const distance_km = distance / 1000;
      const duration_min = duration / 60;

      // 3. Get the human-friendly summary
      const summaryResponse = await axios.post(`${API_BASE_URL}/summary`, {
        distance_km,
        duration_min,
        start_name: "Punto seleccionado A",
        end_name: "Punto seleccionado B"
      });

      setSummary({
        distance_km,
        road_distance_km: road_distance / 1000,
        tree_distance_km: tree_distance / 1000,
        tree_hops: tree_hops,
        summary: summaryResponse.data.summary
      });

    } catch (err) {
      console.error("Error fetching route:", err);
      let message = "Error al calcular la ruta";
      if (err.code === 'ERR_NETWORK') {
        message = "Error de red: ¿Está el servidor backend en ejecución en el puerto 8000?";
      } else if (err.response?.data?.detail) {
        message = err.response.data.detail;
      } else if (err.message) {
        message = err.message;
      }
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative w-screen h-screen overflow-hidden font-sans">
      {/* Map View layer */}
      <MapView 
        onPointsSelected={handlePointsSelected} 
        route={route} 
        treePoints={treePoints}
      />

      {/* Summary Panel overlay */}
      <SummaryPanel 
        loading={loading} 
        error={error} 
        summary={summary} 
      />

      {/* Info Button - Step 8 */}
      <button 
        onClick={() => { setIsFirstVisit(false); setIsInfoModalOpen(true); }}
        className="absolute top-4 right-4 z-[1000] p-3 bg-white hover:bg-gray-50 text-emerald-700 rounded-full shadow-xl transition-all hover:scale-110 active:scale-95 flex items-center justify-center border border-emerald-50"
        title="Más información e instrucciones"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </button>

      {/* Welcome Screen / Info Modal - Step 8 */}
      <InfoModal 
        isOpen={isInfoModalOpen} 
        onClose={() => setIsInfoModalOpen(false)} 
        isWelcome={isFirstVisit}
      />
    </div>
  );
}

export default App;
