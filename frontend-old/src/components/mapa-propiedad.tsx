import L from "leaflet";
import { MapContainer, Marker, Popup, TileLayer, Circle } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import type { LugarTuristico } from "@/lib/types";

const icono = (emoji: string, color: string) =>
  L.divIcon({
    className: "",
    html: `<span style="display:flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:9999px;background:${color};color:#fff;font-size:14px;box-shadow:0 2px 8px rgba(0,0,0,.35)">${emoji}</span>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });

const iconoCasa = icono("⌂", "#1f7a72");
const iconoLugar = icono("★", "#c05a3e");

export function MapaPropiedad({
  lat,
  lng,
  titulo,
  lugares,
}: {
  lat: number;
  lng: number;
  titulo: string;
  lugares: Array<LugarTuristico & { distancia_km: number }>;
}) {
  return (
    <MapContainer
      center={[lat, lng]}
      zoom={12}
      scrollWheelZoom={false}
      className="h-64 w-full rounded-lg"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Circle center={[lat, lng]} radius={800} pathOptions={{ color: "#1f7a72", weight: 1, fillOpacity: 0.08 }} />
      <Marker position={[lat, lng]} icon={iconoCasa}>
        <Popup>{titulo}</Popup>
      </Marker>
      {lugares.map((l) => (
        <Marker key={l.id} position={[l.lat, l.lng]} icon={iconoLugar}>
          <Popup>
            <strong>{l.nombre}</strong>
            <br />
            {l.descripcion}
            <br />
            <em>a {l.distancia_km.toFixed(1)} km</em>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default MapaPropiedad;
