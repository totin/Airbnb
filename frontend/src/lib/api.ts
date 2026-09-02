import type {
  Amenidad,
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

export const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

/* ---------- helpers de red y dominio ---------- */

export const noches = (desde: string, hasta: string) =>
  Math.max(0, Math.round((+new Date(hasta) - +new Date(desde)) / 86_400_000));

const RADIO_TIERRA_KM = 6371;

export function distanciaKm(aLat: number, aLng: number, bLat: number, bLng: number): number {
  const rad = (v: number) => (v * Math.PI) / 180;
  const dLat = rad(bLat - aLat);
  const dLng = rad(bLng - aLng);
  const h =
    Math.sin(dLat / 2) ** 2 + Math.cos(rad(aLat)) * Math.cos(rad(bLat)) * Math.sin(dLng / 2) ** 2;
  return 2 * RADIO_TIERRA_KM * Math.asin(Math.sqrt(h));
}

export function calcularPenalidad(reserva: Reserva, hoy = new Date()): number {
  const horas = (+new Date(reserva.fecha_inicio) - +hoy) / 3_600_000;
  if (horas < 48) return reserva.total;
  if (horas < 24 * 7) return reserva.total * 0.5;
  return 0;
}

async function fetchJson<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = endpoint.startsWith("http") ? endpoint : `${API_URL}${endpoint}`;
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  const res = await fetch(url, { ...options, headers });
  if (!res.ok) {
    let errorDetail = `Error ${res.status}: ${res.statusText}`;
    try {
      const errorJson = await res.json();
      if (errorJson?.detail) {
        errorDetail = typeof errorJson.detail === "string" ? errorJson.detail : JSON.stringify(errorJson.detail);
      }
    } catch {
      /* ignore */
    }
    throw new Error(errorDetail);
  }

  return res.json() as Promise<T>;
}

function formatearUrlImagen(url?: string): string {
  if (!url) return "";
  if (url.startsWith("/uploads/")) {
    return `${API_URL}${url}`;
  }
  return url;
}

function normalizePropiedad(p: any): PropiedadConDatos {
  const imagenes = (p.imagenes || []).map((img: any) =>
    typeof img === "string" ? formatearUrlImagen(img) : formatearUrlImagen(img?.url)
  );

  return {
    ...p,
    id: String(p.id),
    anfitrion_id: String(p.anfitrion_id),
    precio_noche: Number(p.precio_noche),
    capacidad: Number(p.capacidad),
    lat: p.lat != null ? Number(p.lat) : undefined,
    lng: p.lng != null ? Number(p.lng) : undefined,
    imagenes,
    imagen: imagenes[0] || "",
    amenidades: (p.amenidades || []).map(String),
    amenidades_nombres: p.amenidades_nombres || [],
    cantidad_resenas: Number(p.cantidad_resenas || 0),
    promedio_puntaje: p.promedio_puntaje != null ? Number(p.promedio_puntaje) : null,
    anfitrion: p.anfitrion
      ? {
          ...p.anfitrion,
          id: String(p.anfitrion.id),
        }
      : undefined,
  };
}

function normalizeReserva(r: any): ReservaConDatos {
  return {
    ...r,
    id: String(r.id),
    propiedad_id: String(r.propiedad_id),
    huesped_id: String(r.huesped_id),
    total: Number(r.total),
    estado: r.estado as EstadoReserva,
    propiedad: r.propiedad ? normalizePropiedad(r.propiedad) : undefined,
    anfitrion: r.anfitrion
      ? {
          ...r.anfitrion,
          id: String(r.anfitrion.id),
        }
      : undefined,
    huesped: r.huesped
      ? {
          ...r.huesped,
          id: String(r.huesped.id),
        }
      : undefined,
    tiene_resena: Boolean(r.tiene_resena),
  };
}

/* =============================== USUARIOS ================================= */

export async function getUsuarios(): Promise<Usuario[]> {
  const data = await fetchJson<any[]>("/usuarios");
  return data.map((u) => ({
    ...u,
    id: String(u.id),
  }));
}

export async function getUsuarioPorEmail(email: string): Promise<Usuario> {
  const data = await fetchJson<any>(`/usuarios/email/${encodeURIComponent(email)}`);
  return {
    ...data,
    id: String(data.id),
  };
}

export async function getUsuarioPorId(id: string): Promise<Usuario> {
  const data = await fetchJson<any>(`/usuarios/${id}`);
  return {
    ...data,
    id: String(data.id),
  };
}

export async function getUsuarioActual(): Promise<Usuario> {
  const raw = localStorage.getItem("estadia.sesion");
  if (raw) {
    try {
      const u = JSON.parse(raw);
      return await getUsuarioPorId(u.id);
    } catch {
      /* ignore */
    }
  }
  const todos = await getUsuarios();
  if (!todos[0]) {
    throw new Error("No hay usuarios disponibles");
  }
  return todos[0];
}

/** HU1 — Registro de usuario. */
export async function crearUsuario(input: {
  email: string;
  nombre: string;
  es_anfitrion: boolean;
}): Promise<Usuario> {
  const data = await fetchJson<any>("/usuarios", {
    method: "POST",
    body: JSON.stringify(input),
  });
  return {
    ...data,
    id: String(data.id),
  };
}

export async function activarAnfitrionApi(usuarioId: string): Promise<Usuario> {
  const data = await fetchJson<any>(`/anfitriones/${usuarioId}/activar`, {
    method: "PATCH",
  });
  return {
    ...data,
    id: String(data.id),
  };
}

/* ============================== PROPIEDADES =============================== */

/** HU3 — Búsqueda por ciudad, fechas, capacidad, precio y amenidades. */
export async function buscarPropiedades(f: FiltrosBusqueda): Promise<PropiedadConDatos[]> {
  const params = new URLSearchParams();
  if (f.ciudad) params.append("ciudad", f.ciudad);
  if (f.desde) params.append("desde", f.desde);
  if (f.hasta) params.append("hasta", f.hasta);
  if (f.huespedes) params.append("huespedes", String(f.huespedes));
  if (f.precio_max) params.append("precio_max", String(f.precio_max));
  if (f.amenidades?.length) params.append("amenidades", f.amenidades.join(","));

  const qs = params.toString();
  const data = await fetchJson<any[]>(`/propiedades${qs ? `?${qs}` : ""}`);
  return data.map(normalizePropiedad);
}

export async function getPropiedad(id: string): Promise<PropiedadConDatos | undefined> {
  try {
    const data = await fetchJson<any>(`/propiedades/${id}`);
    return normalizePropiedad(data);
  } catch {
    return undefined;
  }
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
  imagenes?: string[];
  lat?: number;
  lng?: number;
}): Promise<PropiedadConDatos> {
  const payload = {
    ...input,
    anfitrion_id: Number(input.anfitrion_id),
  };
  const data = await fetchJson<any>("/propiedades", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return normalizePropiedad(data);
}

/** HU2 — Editar una propiedad (solo el anfitrión dueño). */
export async function actualizarPropiedad(
  id: string,
  anfitrionId: string,
  cambios: Partial<Omit<Propiedad, "id" | "anfitrion_id">>,
): Promise<PropiedadConDatos> {
  const data = await fetchJson<any>(`/propiedades/${id}?anfitrion_id=${anfitrionId}`, {
    method: "PUT",
    body: JSON.stringify(cambios),
  });
  return normalizePropiedad(data);
}

/** HU2 — Borrar una propiedad (solo el anfitrión dueño). */
export async function eliminarPropiedad(id: string, anfitrionId: string): Promise<void> {
  await fetchJson<{ message: string }>(`/propiedades/${id}?anfitrion_id=${anfitrionId}`, {
    method: "DELETE",
  });
}

/** HU2 — Propiedades de un anfitrión. */
export async function getPropiedadesDeAnfitrion(id: string): Promise<PropiedadConDatos[]> {
  const data = await fetchJson<any[]>(`/anfitriones/${id}/propiedades`);
  return data.map(normalizePropiedad);
}

/** HU11 — Top 10 propiedades por ciudad. */
export async function getTopPropiedades(ciudad?: string): Promise<PropiedadConDatos[]> {
  const qs = ciudad ? `?ciudad=${encodeURIComponent(ciudad)}` : "";
  const data = await fetchJson<any[]>(`/propiedades/top${qs}`);
  return data.map(normalizePropiedad);
}

/** HU9 — Calendario de disponibilidad de un mes (YYYY-MM). */
export async function getDisponibilidad(
  propiedadId: string,
  mes: string,
): Promise<DiaDisponibilidad[]> {
  return fetchJson<DiaDisponibilidad[]>(`/propiedades/${propiedadId}/disponibilidad?mes=${mes}`);
}

/* ================================ RESERVAS ================================ */

/** HU4 — Crear reserva. */
export async function crearReserva(input: {
  propiedad_id: string;
  huesped_id: string;
  fecha_inicio: string;
  fecha_fin: string;
  metodo_pago?: string;
}): Promise<ReservaConDatos> {
  const payload = {
    propiedad_id: Number(input.propiedad_id),
    huesped_id: Number(input.huesped_id),
    fecha_inicio: input.fecha_inicio,
    fecha_fin: input.fecha_fin,
    metodo_pago: input.metodo_pago || "dinero",
  };
  const data = await fetchJson<any>("/reservas", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return normalizeReserva(data);
}

/** HU12 — Historial de reservas de un huésped. */
export async function getReservasDeUsuario(
  usuarioId: string,
  estado?: EstadoReserva,
): Promise<ReservaConDatos[]> {
  const qs = estado ? `?estado=${estado}` : "";
  const data = await fetchJson<any[]>(`/reservas/huesped/${usuarioId}${qs}`);
  return data.map(normalizeReserva);
}

/** HU5 — Reservas recibidas por un anfitrión. */
export async function getReservasDeAnfitrion(anfitrionId: string): Promise<ReservaConDatos[]> {
  const data = await fetchJson<any[]>(`/anfitriones/${anfitrionId}/reservas`);
  return data.map(normalizeReserva);
}

/** HU5 — Transiciones de estado de reserva. */
export async function cambiarEstadoReserva(
  reservaId: string,
  nuevo: EstadoReserva,
  actorId?: string,
): Promise<ReservaConDatos> {
  const payload = {
    estado: nuevo,
    actor_id: actorId ? Number(actorId) : undefined,
  };
  const data = await fetchJson<any>(`/reservas/${reservaId}/estado`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
  return normalizeReserva(data);
}

/* ================================ RESEÑAS ================================= */

/** HU6 — Reseñas de una propiedad. */
export async function getResenasDePropiedad(propiedadId: string): Promise<
  Array<Resena & { autor: Usuario | undefined }>
> {
  const data = await fetchJson<any[]>(`/resenas/propiedad/${propiedadId}`);
  return data.map((r) => ({
    ...r,
    id: String(r.id),
    reserva_id: String(r.reserva_id),
    autor_id: String(r.autor_id),
    propiedad_id: String(r.propiedad_id),
    autor: r.autor ? { ...r.autor, id: String(r.autor.id) } : undefined,
  }));
}

/** HU6 — Crear reseña post-estadía. */
export async function crearResena(input: {
  reserva_id: string;
  autor_id: string;
  puntaje: number;
  comentario: string;
}): Promise<Resena> {
  const payload = {
    reserva_id: Number(input.reserva_id),
    autor_id: Number(input.autor_id),
    puntaje: input.puntaje,
    comentario: input.comentario,
  };
  const data = await fetchJson<any>("/resenas", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return {
    ...data,
    id: String(data.id),
    reserva_id: String(data.reserva_id),
    autor_id: String(data.autor_id),
    propiedad_id: String(data.propiedad_id),
  };
}

/* =============================== FAVORITOS ================================ */

/** HU7 — Favoritos de un usuario. */
export async function getFavoritos(usuarioId: string): Promise<PropiedadConDatos[]> {
  const data = await fetchJson<any[]>(`/favoritos/usuario/${usuarioId}`);
  return data.map(normalizePropiedad);
}

export async function agregarFavorito(usuarioId: string, propiedadId: string): Promise<void> {
  await fetchJson<any>("/favoritos", {
    method: "POST",
    body: JSON.stringify({
      usuario_id: Number(usuarioId),
      propiedad_id: Number(propiedadId),
    }),
  });
}

export async function quitarFavorito(usuarioId: string, propiedadId: string): Promise<void> {
  await fetchJson<{ message: string }>(`/favoritos/${usuarioId}/${propiedadId}`, {
    method: "DELETE",
  });
}

/* =============================== AMENIDADES =============================== */

/** HU8 — Lista de amenidades. */
export async function getAmenidades(): Promise<Amenidad[]> {
  const data = await fetchJson<any[]>("/amenidades");
  return data.map((a) => ({
    id: String(a.id),
    nombre: a.nombre,
  }));
}

/* ================================ INGRESOS ================================ */

/** HU10 — Ingresos del anfitrión en un período. */
export async function getIngresos(
  anfitrionId: string,
  desde: string,
  hasta: string,
): Promise<IngresosAnfitrion> {
  const data = await fetchJson<any>(
    `/anfitriones/${anfitrionId}/ingresos?desde=${encodeURIComponent(desde)}&hasta=${encodeURIComponent(hasta)}`
  );
  return {
    total: Number(data.total),
    detalle: (data.detalle || []).map((d: any) => ({
      propiedad_id: String(d.propiedad_id),
      titulo: d.titulo,
      total: Number(d.total),
      reservas: Number(d.reservas),
    })),
  };
}

/* ============================ MAPA TURÍSTICO ============================== */

/** Lugares turísticos destacados. */
export async function getLugares(ciudad?: string): Promise<LugarTuristico[]> {
  const qs = ciudad ? `?ciudad=${encodeURIComponent(ciudad)}` : "";
  const data = await fetchJson<any[]>(`/lugares${qs}`);
  return data.map((l) => ({
    ...l,
    id: String(l.id),
    lat: Number(l.lat),
    lng: Number(l.lng),
  }));
}

/** Lugares con los alojamientos cercanos dentro de un radio (km). */
export async function getLugaresConCercanas(
  ciudad?: string,
  radioKm = 25,
): Promise<LugarConCercanas[]> {
  const params = new URLSearchParams();
  if (ciudad) params.append("ciudad", ciudad);
  params.append("radio_km", String(radioKm));

  const data = await fetchJson<any[]>(`/lugares/cercanias?${params.toString()}`);
  return data.map((l) => ({
    ...l,
    id: String(l.id),
    lat: Number(l.lat),
    lng: Number(l.lng),
    cercanas: (l.cercanas || []).map((c: any) => ({
      ...normalizePropiedad(c),
      distancia_km: Number(c.distancia_km),
    })),
  }));
}

/** Puntos turísticos cercanos a una propiedad. */
export async function getLugaresCercanosAPropiedad(
  propiedadId: string,
  radioKm = 40,
): Promise<Array<LugarTuristico & { distancia_km: number }>> {
  const data = await fetchJson<any[]>(`/propiedades/${propiedadId}/lugares?radio_km=${radioKm}`);
  return data.map((l) => ({
    ...l,
    id: String(l.id),
    lat: Number(l.lat),
    lng: Number(l.lng),
    distancia_km: Number(l.distancia_km),
  }));
}

/* =========================== SALDO DE HORAS =============================== */

export async function getSaldoHoras(usuarioId: string): Promise<number> {
  const data = await fetchJson<any>(`/usuarios/${usuarioId}/horas`);
  return Number(data.horas || 0);
}

export async function sumarHorasApi(usuarioId: string, cantidad: number): Promise<number> {
  const data = await fetchJson<any>(`/usuarios/${usuarioId}/horas/sumar`, {
    method: "POST",
    body: JSON.stringify({ cantidad: Math.round(cantidad) }),
  });
  return Number(data.horas || 0);
}

export async function gastarHorasApi(usuarioId: string, cantidad: number): Promise<number> {
  const data = await fetchJson<any>(`/usuarios/${usuarioId}/horas/gastar`, {
    method: "POST",
    body: JSON.stringify({ cantidad: Math.round(cantidad) }),
  });
  return Number(data.horas || 0);
}

