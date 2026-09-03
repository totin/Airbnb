import type { Amenidad, Favorito, LugarTuristico, Propiedad, Resena, Reserva, Usuario } from "./types";

/**
 * Datos de ejemplo en memoria. Se usan mientras el backend no está conectado.
 * Cuando conectes la API real, borrá este archivo y dejá solo `src/lib/api.ts`.
 */

export const USUARIO_ACTUAL_ID = "u1";

export const usuarios: Usuario[] = [
  { id: "u1", email: "lucia@mail.com", nombre: "Lucía Fernández", fecha_registro: "2025-03-11T10:00:00Z", es_anfitrion: true },
  { id: "u2", email: "martin@mail.com", nombre: "Martín Sosa", fecha_registro: "2025-05-02T10:00:00Z", es_anfitrion: true },
  { id: "u3", email: "cami@mail.com", nombre: "Camila Ruiz", fecha_registro: "2025-06-20T10:00:00Z", es_anfitrion: false },
  { id: "u4", email: "diego@mail.com", nombre: "Diego Paz", fecha_registro: "2026-01-08T10:00:00Z", es_anfitrion: false },
];

export const amenidades: Amenidad[] = [
  { id: "wifi", nombre: "Wifi" },
  { id: "pileta", nombre: "Pileta" },
  { id: "estacionamiento", nombre: "Estacionamiento" },
  { id: "aire", nombre: "Aire acondicionado" },
  { id: "mascotas", nombre: "Acepta mascotas" },
  { id: "cocina", nombre: "Cocina equipada" },
  { id: "lavarropas", nombre: "Lavarropas" },
  { id: "parrilla", nombre: "Parrilla" },
];

export const propiedades: Propiedad[] = [
  {
    id: "p1",
    titulo: "Loft luminoso en Palermo Soho",
    direccion: "Gurruchaga 1840",
    ciudad: "Buenos Aires",
    precio_noche: 48000,
    capacidad: 3,
    anfitrion_id: "u1",
    lat: -34.5885,
    lng: -58.4306,
    amenidades: ["wifi", "aire", "cocina", "lavarropas"],
  },
  {
    id: "p2",
    titulo: "Casa con pileta y parrilla",
    direccion: "Los Álamos 320",
    ciudad: "Córdoba",
    precio_noche: 72000,
    capacidad: 6,
    anfitrion_id: "u1",
    lat: -31.38,
    lng: -64.53,
    amenidades: ["wifi", "pileta", "parrilla", "estacionamiento", "cocina"],
  },
  {
    id: "p3",
    titulo: "Cabaña de montaña frente al lago",
    direccion: "Camino de los Nogales 55",
    ciudad: "Bariloche",
    precio_noche: 95000,
    capacidad: 4,
    anfitrion_id: "u2",
    lat: -41.118,
    lng: -71.34,
    amenidades: ["wifi", "estacionamiento", "mascotas", "parrilla"],
  },
  {
    id: "p4",
    titulo: "Depto frente al mar",
    direccion: "Bv. Marítimo 2100",
    ciudad: "Mar del Plata",
    precio_noche: 56000,
    capacidad: 5,
    anfitrion_id: "u2",
    lat: -38.01,
    lng: -57.535,
    amenidades: ["wifi", "aire", "cocina", "estacionamiento"],
  },
  {
    id: "p5",
    titulo: "Estudio minimalista en San Telmo",
    direccion: "Defensa 780",
    ciudad: "Buenos Aires",
    precio_noche: 32000,
    capacidad: 2,
    anfitrion_id: "u2",
    lat: -34.62,
    lng: -58.372,
    amenidades: ["wifi", "cocina"],
  },
  {
    id: "p6",
    titulo: "Finca con viñedos y pileta",
    direccion: "Ruta 15 km 4",
    ciudad: "Mendoza",
    precio_noche: 110000,
    capacidad: 8,
    anfitrion_id: "u1",
    lat: -33.05,
    lng: -68.88,
    amenidades: ["wifi", "pileta", "parrilla", "estacionamiento", "mascotas", "cocina"],
  },
];

export const reservas: Reserva[] = [
  { id: "r1", propiedad_id: "p1", huesped_id: "u3", fecha_inicio: "2026-08-20", fecha_fin: "2026-08-24", estado: "confirmada", total: 192000 },
  { id: "r2", propiedad_id: "p2", huesped_id: "u3", fecha_inicio: "2026-09-02", fecha_fin: "2026-09-06", estado: "pendiente", total: 288000 },
  { id: "r3", propiedad_id: "p3", huesped_id: "u1", fecha_inicio: "2026-06-10", fecha_fin: "2026-06-15", estado: "confirmada", total: 475000 },
  { id: "r4", propiedad_id: "p4", huesped_id: "u1", fecha_inicio: "2026-07-01", fecha_fin: "2026-07-05", estado: "confirmada", total: 224000 },
  { id: "r5", propiedad_id: "p1", huesped_id: "u4", fecha_inicio: "2026-05-11", fecha_fin: "2026-05-14", estado: "confirmada", total: 144000 },
  { id: "r6", propiedad_id: "p1", huesped_id: "u3", fecha_inicio: "2026-04-02", fecha_fin: "2026-04-06", estado: "confirmada", total: 192000 },
  { id: "r7", propiedad_id: "p6", huesped_id: "u4", fecha_inicio: "2026-08-14", fecha_fin: "2026-08-18", estado: "pendiente", total: 440000 },
  { id: "r8", propiedad_id: "p2", huesped_id: "u4", fecha_inicio: "2026-03-01", fecha_fin: "2026-03-04", estado: "confirmada", total: 216000 },
];

export const resenas: Resena[] = [
  { id: "re1", reserva_id: "r5", autor_id: "u4", propiedad_id: "p1", puntaje: 5, comentario: "Impecable, muy bien ubicado.", fecha: "2026-05-15T12:00:00Z" },
  { id: "re2", reserva_id: "r6", autor_id: "u3", propiedad_id: "p1", puntaje: 4, comentario: "Muy lindo, un poco ruidoso de noche.", fecha: "2026-04-07T12:00:00Z" },
  { id: "re3", reserva_id: "r8", autor_id: "u4", propiedad_id: "p2", puntaje: 5, comentario: "La pileta es un golazo.", fecha: "2026-03-05T12:00:00Z" },
  { id: "re4", reserva_id: "r3", autor_id: "u1", propiedad_id: "p3", puntaje: 5, comentario: "Vista increíble al lago.", fecha: "2026-06-16T12:00:00Z" },
  { id: "re5", reserva_id: "r4", autor_id: "u1", propiedad_id: "p4", puntaje: 3, comentario: "Cumple, pero necesita mantenimiento.", fecha: "2026-07-06T12:00:00Z" },
];

export const favoritos: Favorito[] = [
  { usuario_id: "u1", propiedad_id: "p3", fecha: "2026-07-20T12:00:00Z" },
  { usuario_id: "u1", propiedad_id: "p4", fecha: "2026-07-22T12:00:00Z" },
];
/** Lugares turísticos destacados (HU extra — mapa interactivo). */
export const lugares: LugarTuristico[] = [
  { id: "l1", nombre: "Caminito, La Boca", ciudad: "Buenos Aires", descripcion: "Calle museo con casas de colores, tango y arte callejero.", categoria: "Cultura", lat: -34.6395, lng: -58.3625 },
  { id: "l2", nombre: "Bosques de Palermo", ciudad: "Buenos Aires", descripcion: "Parques, lago y rosedal en el corazón de la ciudad.", categoria: "Naturaleza", lat: -34.5711, lng: -58.4171 },
  { id: "l3", nombre: "Cerro Catedral", ciudad: "Bariloche", descripcion: "El centro de esquí más grande de Sudamérica.", categoria: "Aventura", lat: -41.1670, lng: -71.4400 },
  { id: "l4", nombre: "Villa Carlos Paz", ciudad: "Córdoba", descripcion: "Lago San Roque, teatros y vida nocturna serrana.", categoria: "Sierras", lat: -31.4241, lng: -64.4978 },
  { id: "l5", nombre: "Playa Bristol", ciudad: "Mar del Plata", descripcion: "La playa clásica marplatense frente al casino.", categoria: "Playa", lat: -38.0055, lng: -57.5426 },
  { id: "l6", nombre: "Ruta del Vino de Luján", ciudad: "Mendoza", descripcion: "Bodegas y viñedos con la cordillera de fondo.", categoria: "Gastronomía", lat: -33.0400, lng: -68.9300 },
];
