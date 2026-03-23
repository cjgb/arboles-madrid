import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Polyline, CircleMarker, useMapEvents } from 'react-leaflet';
import L from 'leaflet';

// Fix Leaflet marker icons with imports from leaflet dist
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl,
  iconUrl,
  shadowUrl,
});

/**
 * Component to handle map clicks for selecting start/end points.
 */
function MapClickHandler({ onClick }) {
  useMapEvents({
    click(e) {
      onClick(e.latlng);
    },
  });
  return null;
}

/**
 * Creates a DivIcon for markers with a color and letter.
 */
const createMarkerIcon = (color, label) => {
  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div style="
        background-color: ${color};
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        border: 2px solid white;
        box-shadow: 0 0 4px rgba(0,0,0,0.4);
      ">
        ${label}
      </div>
    `,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
  });
};

const MapView = ({ onPointsSelected, route, treePoints }) => {
  const [start, setStart] = useState(null);
  const [end, setEnd] = useState(null);

  const handleMapClick = (latlng) => {
    if (!start) {
      setStart(latlng);
    } else if (!end) {
      setEnd(latlng);
      // ORS expects [lon, lat]
      onPointsSelected(
        [start.lng, start.lat],
        [latlng.lng, latlng.lat]
      );
    } else {
      // Reset
      setStart(null);
      setEnd(null);
    }
  };

  return (
    <div className="w-full h-screen">
      <MapContainer
        center={[40.4168, -3.7038]}
        zoom={13}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        
        <MapClickHandler onClick={handleMapClick} />

        {start && (
          <Marker
            position={start}
            icon={createMarkerIcon('#22c55e', 'A')} // Tailwind green-500
          />
        )}

        {end && (
          <Marker
            position={end}
            icon={createMarkerIcon('#ef4444', 'B')} // Tailwind red-500
          />
        )}

        {route && (
          <Polyline
            positions={route}
            color="#2563eb" // Bright blue
            weight={6}
            opacity={0.5} // More transparent to see dots better
          />
        )}

        {treePoints && treePoints.map((point, idx) => (
          <CircleMarker
            key={idx}
            center={[point[1], point[0]]}
            radius={5} // Bigger radius
            pathOptions={{ 
              color: '#064e3b', // Dark green stroke
              fillColor: '#10b981', // Bright emerald/forest green fill
              fillOpacity: 1, 
              weight: 2 
            }}
          />
        ))}
      </MapContainer>
    </div>
  );
};

export default MapView;
