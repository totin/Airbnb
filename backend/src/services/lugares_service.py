import math
from typing import Optional
from sqlalchemy.orm import Session
from src.dtos.lugares_dto import LugarTuristicoDTO, LugarCercanoDTO, LugarConCercanasDTO
from src.services.propiedad_service import PropiedadService

RADIO_TIERRA_KM = 6371.0


def distancia_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calcula la distancia geodésica en kilómetros mediante la fórmula de Haversine."""
    rad = math.radians
    d_lat = rad(lat2 - lat1)
    d_lng = rad(lng2 - lng1)
    a = (
        math.sin(d_lat / 2.0) ** 2
        + math.cos(rad(lat1)) * math.cos(rad(lat2)) * math.sin(d_lng / 2.0) ** 2
    )
    c = 2.0 * math.asin(math.sqrt(a))
    return round(RADIO_TIERRA_KM * c, 2)


LUGARES_DATA = [
    {
        "id": "l1",
        "nombre": "Caminito, La Boca",
        "ciudad": "Buenos Aires",
        "descripcion": "Calle museo con casas de colores, tango y arte callejero.",
        "categoria": "Cultura",
        "lat": -34.6395,
        "lng": -58.3625,
    },
    {
        "id": "l2",
        "nombre": "Bosques de Palermo",
        "ciudad": "Buenos Aires",
        "descripcion": "Parques, lago y rosedal en el corazón de la ciudad.",
        "categoria": "Naturaleza",
        "lat": -34.5711,
        "lng": -58.4171,
    },
    {
        "id": "l3",
        "nombre": "Cerro Catedral",
        "ciudad": "Bariloche",
        "descripcion": "El centro de esquí más grande de Sudamérica.",
        "categoria": "Aventura",
        "lat": -41.1670,
        "lng": -71.4400,
    },
    {
        "id": "l4",
        "nombre": "Villa Carlos Paz",
        "ciudad": "Córdoba",
        "descripcion": "Lago San Roque, teatros y vida nocturna serrana.",
        "categoria": "Sierras",
        "lat": -31.4241,
        "lng": -64.4978,
    },
    {
        "id": "l5",
        "nombre": "Playa Bristol",
        "ciudad": "Mar del Plata",
        "descripcion": "La playa clásica marplatense frente al casino.",
        "categoria": "Playa",
        "lat": -38.0055,
        "lng": -57.5426,
    },
    {
        "id": "l6",
        "nombre": "Ruta del Vino de Luján",
        "ciudad": "Mendoza",
        "descripcion": "Bodegas y viñedos con la cordillera de fondo.",
        "categoria": "Gastronomía",
        "lat": -33.0400,
        "lng": -68.9300,
    },
]


class LugaresService:
    def listar_lugares(self, ciudad: Optional[str] = None) -> list[dict]:
        if ciudad:
            c = ciudad.strip().lower()
            return [l for l in LUGARES_DATA if l["ciudad"].lower() == c]
        return LUGARES_DATA

    def get_lugares_cercanos_a_propiedad(
        self,
        lat: Optional[float],
        lng: Optional[float],
        radio_km: float = 40.0,
    ) -> list[dict]:
        if lat is None or lng is None:
            return []

        resultado = []
        for l in LUGARES_DATA:
            dist = distancia_km(lat, lng, l["lat"], l["lng"])
            if dist <= radio_km:
                resultado.append({**l, "distancia_km": dist})

        resultado.sort(key=lambda x: x["distancia_km"])
        return resultado

    def get_lugares_con_cercanias(
        self,
        db: Session,
        ciudad: Optional[str] = None,
        radio_km: float = 25.0,
    ) -> list[dict]:
        prop_service = PropiedadService(db)
        props = prop_service.buscar_propiedades(ciudad=ciudad)

        lugares = self.listar_lugares(ciudad=ciudad)
        resultado = []

        for l in lugares:
            cercanas = []
            for p in props:
                p_lat = p.get("lat")
                p_lng = p.get("lng")
                if p_lat is not None and p_lng is not None:
                    dist = distancia_km(l["lat"], l["lng"], p_lat, p_lng)
                    if dist <= radio_km:
                        cercanas.append({**p, "distancia_km": dist})

            cercanas.sort(key=lambda x: x["distancia_km"])
            resultado.append({**l, "cercanas": cercanas})

        return resultado
