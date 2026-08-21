// Tipos del dominio (Proyecto 1 — Airbnb)

export type EstadoReserva = "pendiente" | "confirmada" | "rechazada" | "cancelada";

export interface Usuario {
  id: string;
  email: string;
  nombre: string;
  fecha_registro: string; // ISO
  es_anfitrion: boolean;
}

export interface Amenidad {
  id: string;
  nombre: string;
}

export interface Propiedad {
  id: string;
  titulo: string;
  direccion: string;
  ciudad: string;
  precio_noche: number;
  capacidad: number;
  anfitrion_id: string;
  imagen?: string;
  lat?: number;
  lng?: number;
  amenidades: string[]; // ids de amenidad (N a M propiedad_amenidades)
}

export interface Reserva {
  id: string;
  propiedad_id: string;
  huesped_id: string;
  fecha_inicio: string; // YYYY-MM-DD
  fecha_fin: string; // YYYY-MM-DD
  estado: EstadoReserva;
  total: number;
}

export interface Resena {
  id: string;
  reserva_id: string;
  autor_id: string;
  propiedad_id: string;
  puntaje: number; // 1..5
  comentario: string;
  fecha: string; // ISO
}

export interface Favorito {
  usuario_id: string;
  propiedad_id: string;
  fecha: string; // ISO
}

/** Propiedad enriquecida para las vistas de búsqueda / detalle. */
export interface PropiedadConDatos extends Propiedad {
  anfitrion: Usuario | undefined;
  promedio_puntaje: number | null;
  cantidad_resenas: number;
  amenidades_nombres: string[];
}

/** Reserva enriquecida (HU12: incluye propiedad y anfitrión). */
export interface ReservaConDatos extends Reserva {
  propiedad: Propiedad | undefined;
  anfitrion: Usuario | undefined;
  huesped: Usuario | undefined;
  tiene_resena: boolean;
}

export interface FiltrosBusqueda {
  ciudad?: string | undefined;
  desde?: string | undefined;
  hasta?: string | undefined;
  huespedes?: number | undefined;
  precio_max?: number | undefined;
  amenidades?: string[] | undefined;
}

export interface DiaDisponibilidad {
  fecha: string; // YYYY-MM-DD
  ocupado: boolean;
}

export interface IngresosAnfitrion {
  total: number;
  detalle: Array<{ propiedad_id: string; titulo: string; total: number; reservas: number }>;
}
/** Punto turístico destacado para el mapa interactivo. */
export interface LugarTuristico {
  id: string;
  nombre: string;
  ciudad: string;
  descripcion: string;
  categoria: string;
  lat: number;
  lng: number;
}

/** Lugar turístico + alojamientos cercanos (con distancia en km). */
export interface LugarConCercanas extends LugarTuristico {
  cercanas: Array<PropiedadConDatos & { distancia_km: number }>;
}
