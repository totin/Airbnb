import * as db from "./mock-data";
import type {
  DiaDisponibilidad,
  EstadoReserva,
  FiltrosBusqueda,
  IngresosAnfitrion,
  LugarConCercanas,
  LugarTuristico,
  Propiedad,
  PropiedadConDatos,
  Resena,
  Reserva,
  ReservaConDatos,
  Usuario,
} from "./types";

/* =============================================================================
 * CAPA DE API
 * -----------------------------------------------------------------------------
 * Cada función tiene arriba, comentado, el endpoint REST que debería consumir.
 * Para conectar el backend real: descomentá el bloque `fetch` y borrá la
 * implementación mock de abajo. La firma y el tipo de retorno no cambian.
 *
 * export const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
 * ========================================================================== */

export const API_URL = "http://localhost:8000";

const delay = (ms = 180) => new Promise((r) => setTimeout(r, ms));
const uid = () => Math.random().toString(36).slice(2, 9);

/* ---------- helpers de dominio (mock) ---------- */

export const noches = (desde: string, hasta: string) =>
  Math.max(0, Math.round((+new Date(hasta) - +new Date(desde)) / 86_400_000));

const seSolapan = (aIni: string, aFin: string, bIni: string, bFin: string) =>
  new Date(aIni) < new Date(bFin) && new Date(bIni) < new Date(aFin);

function enriquecerPropiedad(p: Propiedad): PropiedadConDatos {
  const rs = db.resenas.filter((r) => r.propiedad_id === p.id);
  return {
    ...p,
    anfitrion: db.usuarios.find((u) => u.id === p.anfitrion_id),
    cantidad_resenas: rs.length,
    promedio_puntaje: rs.length ? rs.reduce((a, r) => a + r.puntaje, 0) / rs.length : null,
    amenidades_nombres: (p.amenidades ?? []).map(
  (id) => db.amenidades.find((a) => a.id === id)?.nombre ?? id,
    ),
  };
}

function enriquecerReserva(r: Reserva): ReservaConDatos {
  const propiedad = db.propiedades.find((p) => p.id === r.propiedad_id);
  return {
    ...r,
    propiedad,
    anfitrion: db.usuarios.find((u) => u.id === propiedad?.anfitrion_id),
    huesped: db.usuarios.find((u) => u.id === r.huesped_id),
    tiene_resena: db.resenas.some((re) => re.reserva_id === r.id),
  };
}

/* =============================== USUARIOS ================================= */

export async function getUsuarioActual(): Promise<Usuario> {
  // GET /usuarios/me
  // return fetch(`${API_URL}/usuarios/me`).then((r) => r.json());
  await delay(60);
  return db.usuarios.find((u) => u.id === db.USUARIO_ACTUAL_ID)!;
}

/** HU1 — Registro de usuario. */
export async function crearUsuario(input: {
  email: string;
  nombre: string;
  es_anfitrion: boolean;
}): Promise<Usuario> {
  // POST /usuarios  -> 201 { id, email, nombre, fecha_registro, es_anfitrion }
  // return fetch(`${API_URL}/usuarios`, {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify(input),
  // }).then((r) => r.json());
  await delay();
  if (db.usuarios.some((u) => u.email.toLowerCase() === input.email.toLowerCase())) {
    throw new Error("Ya existe un usuario con ese email");
  }
  const nuevo: Usuario = {
    id: uid(),
    email: input.email,
    nombre: input.nombre,
    es_anfitrion: input.es_anfitrion,
    fecha_registro: new Date().toISOString(),
  };
  db.usuarios.push(nuevo);
  return nuevo;
}

/* ============================== PROPIEDADES =============================== */

/** HU3 — Búsqueda por ciudad, fechas, capacidad, precio y amenidades. */
export async function buscarPropiedades(f: FiltrosBusqueda): Promise<PropiedadConDatos[]> {
  const qs = new URLSearchParams();
  if (f.ciudad) qs.set("ciudad", f.ciudad);
  if (f.huespedes) qs.set("capacidad_minima", String(f.huespedes));

  const res = await fetch(`${API_URL}/propiedades?${qs}`);
  const propiedades: Propiedad[] = await res.json();
  return propiedades.map(enriquecerPropiedad);
}

export async function getPropiedad(id: string): Promise<PropiedadConDatos | undefined> {
  // GET /propiedades/{id}
  // return fetch(`${API_URL}/propiedades/${id}`).then((r) => r.json());
  await delay(120);
  const p = db.propiedades.find((x) => x.id === id);
  return p ? enriquecerPropiedad(p) : undefined;
}

/** HU2 — Publicar propiedad (solo anfitriones). */
export async function crearPropiedad(input: {
  titulo: string;
  direccion: string;
  ciudad: string;
  precio_noche: number;
  capacidad: number;
  anfitrion_id: string;
  amenidades: string[];
}): Promise<Propiedad> {
  // POST /propiedades -> 201
  // return fetch(`${API_URL}/propiedades`, { method: "POST", ... }).then((r) => r.json());
  await delay();
  const anfitrion = db.usuarios.find((u) => u.id === input.anfitrion_id);
  if (!anfitrion?.es_anfitrion) throw new Error("Solo un anfitrión puede publicar propiedades");
  if (input.precio_noche <= 0) throw new Error("El precio por noche debe ser mayor a 0");
  if (input.capacidad <= 0) throw new Error("La capacidad debe ser mayor a 0");
  const nueva: Propiedad = { id: uid(), ...input };
  db.propiedades.push(nueva);
  return nueva;
}

/** HU2 — Propiedades de un anfitrión. */
export async function getPropiedadesDeAnfitrion(id: string): Promise<PropiedadConDatos[]> {
  // GET /anfitriones/{id}/propiedades
  await delay(120);
  return db.propiedades.filter((p) => p.anfitrion_id === id).map(enriquecerPropiedad);
}

/** HU11 — Top 10 propiedades por ciudad (mín. 3 reseñas). */
export async function getTopPropiedades(ciudad?: string): Promise<PropiedadConDatos[]> {
  // GET /propiedades/top?ciudad=X
  await delay(120);
  return db.propiedades
    .filter((p) => (ciudad ? p.ciudad === ciudad : true))
    .map(enriquecerPropiedad)
    .filter((p) => p.cantidad_resenas >= 3)
    .sort((a, b) => (b.promedio_puntaje ?? 0) - (a.promedio_puntaje ?? 0))
    .slice(0, 10);
}

/** HU9 — Calendario de disponibilidad de un mes (YYYY-MM). */
export async function getDisponibilidad(
  propiedadId: string,
  mes: string,
): Promise<DiaDisponibilidad[]> {
  // GET /propiedades/{id}/disponibilidad?mes=YYYY-MM
  await delay(120);
  const [y, m] = mes.split("-").map(Number) as [number, number];
  const dias = new Date(y, m, 0).getDate();
  const ocupadas = db.reservas.filter(
    (r) => r.propiedad_id === propiedadId && r.estado === "confirmada",
  );
  return Array.from({ length: dias }, (_, i) => {
    const fecha = `${mes}-${String(i + 1).padStart(2, "0")}`;
    return {
      fecha,
      ocupado: ocupadas.some((r) => fecha >= r.fecha_inicio && fecha < r.fecha_fin),
    };
  });
}

/* ================================ RESERVAS ================================ */

/** HU4 — Crear reserva. */
export async function crearReserva(input: {
  propiedad_id: string;
  huesped_id: string;
  fecha_inicio: string;
  fecha_fin: string;
}): Promise<Reserva> {
  // POST /reservas -> 201
  await delay();
  const prop = db.propiedades.find((p) => p.id === input.propiedad_id);
  if (!prop) throw new Error("La propiedad no existe");
  if (prop.anfitrion_id === input.huesped_id)
    throw new Error("No podés reservar tu propia propiedad");
  if (!(new Date(input.fecha_inicio) < new Date(input.fecha_fin)))
    throw new Error("La fecha de inicio debe ser anterior a la de fin");
  const solapa = db.reservas.some(
    (r) =>
      r.propiedad_id === prop.id &&
      r.estado === "confirmada" &&
      seSolapan(input.fecha_inicio, input.fecha_fin, r.fecha_inicio, r.fecha_fin),
  );
  if (solapa) throw new Error("Ya existe una reserva confirmada en ese rango");
  const nueva: Reserva = {
    id: uid(),
    ...input,
    estado: "pendiente",
    total: prop.precio_noche * noches(input.fecha_inicio, input.fecha_fin),
  };
  db.reservas.push(nueva);
  return nueva;
}

/** HU12 — Historial de reservas de un huésped. */
export async function getReservasDeUsuario(
  usuarioId: string,
  estado?: EstadoReserva,
): Promise<ReservaConDatos[]> {
  // GET /usuarios/{id}/reservas?estado=confirmada
  await delay(120);
  return db.reservas
    .filter((r) => r.huesped_id === usuarioId)
    .filter((r) => (estado ? r.estado === estado : true))
    .sort((a, b) => b.fecha_inicio.localeCompare(a.fecha_inicio))
    .map(enriquecerReserva);
}

/** HU5 — Reservas recibidas por un anfitrión. */
export async function getReservasDeAnfitrion(anfitrionId: string): Promise<ReservaConDatos[]> {
  // GET /anfitriones/{id}/reservas
  await delay(120);
  const ids = db.propiedades.filter((p) => p.anfitrion_id === anfitrionId).map((p) => p.id);
  return db.reservas
    .filter((r) => ids.includes(r.propiedad_id))
    .sort((a, b) => b.fecha_inicio.localeCompare(a.fecha_inicio))
    .map(enriquecerReserva);
}

/** HU5 — Transiciones de estado: pendiente→confirmada|rechazada, confirmada→cancelada.
 *  `actorId` (opcional) valida permisos: confirmar/rechazar solo el anfitrión dueño;
 *  cancelar el anfitrión dueño o el huésped de la reserva. */
export async function cambiarEstadoReserva(
  reservaId: string,
  nuevo: EstadoReserva,
  actorId?: string,
): Promise<Reserva> {
  // PATCH /reservas/{id}/estado  body: { estado }
  // (o POST /reservas/{id}/confirmar | /rechazar | /cancelar)
  await delay();
  const r = db.reservas.find((x) => x.id === reservaId);
  if (!r) throw new Error("Reserva inexistente");
  const validas: Record<string, EstadoReserva[]> = {
    pendiente: ["confirmada", "rechazada"],
    confirmada: ["cancelada"],
    rechazada: [],
    cancelada: [],
  };
  if (!(validas[r.estado] ?? []).includes(nuevo))
    throw new Error(`Transición inválida: ${r.estado} → ${nuevo}`);
  if (actorId) {
    const prop = db.propiedades.find((p) => p.id === r.propiedad_id);
    const esDuenio = prop?.anfitrion_id === actorId;
    const esHuesped = r.huesped_id === actorId;
    if ((nuevo === "confirmada" || nuevo === "rechazada") && !esDuenio)
      throw new Error("Solo el anfitrión dueño puede confirmar o rechazar la reserva");
    if (nuevo === "cancelada" && !esDuenio && !esHuesped)
      throw new Error("No podés cancelar esta reserva");
  }
  r.estado = nuevo;
  return r;
}


/** HU5 — Penalidad por cancelación: <48hs = 100%, <7 días = 50%, si no 0%. */
export function calcularPenalidad(reserva: Reserva, hoy = new Date()): number {
  const horas = (+new Date(reserva.fecha_inicio) - +hoy) / 3_600_000;
  if (horas < 48) return reserva.total;
  if (horas < 24 * 7) return reserva.total * 0.5;
  return 0;
}

/* ================================ RESEÑAS ================================= */

/** HU6 — Reseñas de una propiedad. */
export async function getResenasDePropiedad(propiedadId: string): Promise<
  Array<Resena & { autor: Usuario | undefined }>
> {
  // GET /propiedades/{id}/resenas
  await delay(120);
  return db.resenas
    .filter((r) => r.propiedad_id === propiedadId)
    .sort((a, b) => b.fecha.localeCompare(a.fecha))
    .map((r) => ({ ...r, autor: db.usuarios.find((u) => u.id === r.autor_id) }));
}

/** HU6 — Crear reseña post-estadía. */
export async function crearResena(input: {
  reserva_id: string;
  autor_id: string;
  puntaje: number;
  comentario: string;
}): Promise<Resena> {
  // POST /reservas/{reserva_id}/resenas -> 201
  await delay();
  const reserva = db.reservas.find((r) => r.id === input.reserva_id);
  if (!reserva) throw new Error("Reserva inexistente");
  if (reserva.huesped_id !== input.autor_id)
    throw new Error("Solo el huésped de la reserva puede dejar la reseña");
  if (reserva.estado !== "confirmada") throw new Error("Solo se reseñan reservas confirmadas");
  if (new Date(reserva.fecha_fin) >= new Date()) throw new Error("La estadía todavía no terminó");
  if (db.resenas.some((r) => r.reserva_id === reserva.id))
    throw new Error("Esta reserva ya tiene una reseña");
  if (input.puntaje < 1 || input.puntaje > 5) throw new Error("El puntaje debe estar entre 1 y 5");
  const nueva: Resena = {
    id: uid(),
    reserva_id: reserva.id,
    autor_id: input.autor_id,
    propiedad_id: reserva.propiedad_id,
    puntaje: input.puntaje,
    comentario: input.comentario,
    fecha: new Date().toISOString(),
  };
  db.resenas.push(nueva);
  return nueva;
}

/* =============================== FAVORITOS ================================ */

/** HU7 — Favoritos de un usuario. */
export async function getFavoritos(usuarioId: string): Promise<PropiedadConDatos[]> {
  // GET /usuarios/{id}/favoritos
  await delay(120);
  return db.favoritos
    .filter((f) => f.usuario_id === usuarioId)
    .map((f) => db.propiedades.find((p) => p.id === f.propiedad_id))
    .filter((p): p is Propiedad => Boolean(p))
    .map(enriquecerPropiedad);
}

export async function agregarFavorito(usuarioId: string, propiedadId: string): Promise<void> {
  // POST /usuarios/{id}/favoritos  body: { propiedad_id }
  await delay(100);
  if (db.favoritos.some((f) => f.usuario_id === usuarioId && f.propiedad_id === propiedadId))
    throw new Error("Ya está en favoritos");
  db.favoritos.push({
    usuario_id: usuarioId,
    propiedad_id: propiedadId,
    fecha: new Date().toISOString(),
  });
}

export async function quitarFavorito(usuarioId: string, propiedadId: string): Promise<void> {
  // DELETE /usuarios/{id}/favoritos/{propiedad_id}
  await delay(100);
  const i = db.favoritos.findIndex(
    (f) => f.usuario_id === usuarioId && f.propiedad_id === propiedadId,
  );
  if (i >= 0) db.favoritos.splice(i, 1);
}

/* =============================== AMENIDADES =============================== */

/** HU8 — Lista fija de amenidades. */
export async function getAmenidades() {
  // GET /amenidades
  await delay(60);
  return db.amenidades;
}

/* ================================ INGRESOS ================================ */

/** HU10 — Ingresos del anfitrión en un período. */
export async function getIngresos(
  anfitrionId: string,
  desde: string,
  hasta: string,
): Promise<IngresosAnfitrion> {
  // GET /anfitriones/{id}/ingresos?desde=YYYY-MM-DD&hasta=YYYY-MM-DD
  await delay(150);
  const props = db.propiedades.filter((p) => p.anfitrion_id === anfitrionId);
  const detalle = props.map((p) => {
    const rs = db.reservas.filter(
      (r) =>
        r.propiedad_id === p.id &&
        r.estado === "confirmada" &&
        r.fecha_fin >= desde &&
        r.fecha_fin <= hasta,
    );
    return {
      propiedad_id: p.id,
      titulo: p.titulo,
      total: rs.reduce((a, r) => a + r.total, 0),
      reservas: rs.length,
    };
  });
  return { total: detalle.reduce((a, d) => a + d.total, 0), detalle };
}
/* ============================ MAPA TURÍSTICO ============================== */

const RADIO_TIERRA_KM = 6371;

/** Distancia en km entre dos coordenadas (haversine). */
export function distanciaKm(aLat: number, aLng: number, bLat: number, bLng: number): number {
  const rad = (v: number) => (v * Math.PI) / 180;
  const dLat = rad(bLat - aLat);
  const dLng = rad(bLng - aLng);
  const h =
    Math.sin(dLat / 2) ** 2 + Math.cos(rad(aLat)) * Math.cos(rad(bLat)) * Math.sin(dLng / 2) ** 2;
  return 2 * RADIO_TIERRA_KM * Math.asin(Math.sqrt(h));
}

/** Lugares turísticos destacados. */
export async function getLugares(ciudad?: string): Promise<LugarTuristico[]> {
  // GET /lugares?ciudad=X
  // return fetch(`${API_URL}/lugares?ciudad=${ciudad ?? ""}`).then((r) => r.json());
  await delay(80);
  return db.lugares.filter((l) => (ciudad ? l.ciudad === ciudad : true));
}

/** Lugares con los alojamientos cercanos dentro de un radio (km). */
export async function getLugaresConCercanas(
  ciudad?: string,
  radioKm = 25,
): Promise<LugarConCercanas[]> {
  // GET /lugares/cercanias?ciudad=X&radio_km=25
  // return fetch(`${API_URL}/lugares/cercanias?ciudad=${ciudad ?? ""}&radio_km=${radioKm}`)
  //   .then((r) => r.json());
  await delay(140);
  return db.lugares
    .filter((l) => (ciudad ? l.ciudad === ciudad : true))
    .map((l) => ({
      ...l,
      cercanas: db.propiedades
        .filter((p) => p.lat != null && p.lng != null)
        .map((p) => ({
          ...enriquecerPropiedad(p),
          distancia_km: distanciaKm(l.lat, l.lng, p.lat!, p.lng!),
        }))
        .filter((p) => p.distancia_km <= radioKm)
        .sort((a, b) => a.distancia_km - b.distancia_km),
    }));
}

/** Puntos turísticos cercanos a una propiedad (para el mini mapa del detalle). */
export async function getLugaresCercanosAPropiedad(
  propiedadId: string,
  radioKm = 40,
): Promise<Array<LugarTuristico & { distancia_km: number }>> {
  // GET /propiedades/{id}/lugares?radio_km=40
  // return fetch(`${API_URL}/propiedades/${propiedadId}/lugares?radio_km=${radioKm}`)
  //   .then((r) => r.json());
  await delay(100);
  const p = db.propiedades.find((x) => x.id === propiedadId);
  if (!p || p.lat == null || p.lng == null) return [];
  return db.lugares
    .map((l) => ({ ...l, distancia_km: distanciaKm(p.lat!, p.lng!, l.lat, l.lng) }))
    .filter((l) => l.distancia_km <= radioKm)
    .sort((a, b) => a.distancia_km - b.distancia_km);
}
