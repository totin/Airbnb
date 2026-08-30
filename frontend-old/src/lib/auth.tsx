import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { usuarios } from "./mock-data";
import type { Usuario } from "./types";

/**
 * Sesión de usuario (mock, en localStorage).
 * Endpoints reales sugeridos:
 *  - POST /auth/login   { email } -> 200 { usuario, token }
 *  - POST /auth/logout  -> 204
 *  - GET  /usuarios/me  -> 200 usuario
 */

export type Rol = "huesped" | "anfitrion";

interface Sesion {
  usuario: Usuario | null;
  rol: Rol | null;
  esAnfitrion: boolean;
  cargando: boolean;
  login: (email: string) => Promise<Usuario>;
  logout: () => void;
  /** PATCH /usuarios/{id} { es_anfitrion: true } */
  activarAnfitrion: () => void;
}

const STORAGE_KEY = "estadia.sesion";
const SesionCtx = createContext<Sesion | null>(null);

export function SesionProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) setUsuario(JSON.parse(raw) as Usuario);
    } catch {
      /* noop */
    }
    setCargando(false);
  }, []);

  const login = useCallback(async (email: string) => {
    // POST /auth/login { email }
    const u = usuarios.find((x) => x.email.toLowerCase() === email.trim().toLowerCase());
    if (!u) throw new Error("No existe una cuenta con ese email");
    setUsuario(u);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(u));
    return u;
  }, []);

  const logout = useCallback(() => {
    // POST /auth/logout
    setUsuario(null);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  const activarAnfitrion = useCallback(() => {
    // PATCH /usuarios/{id} { es_anfitrion: true }
    setUsuario((u) => {
      if (!u) return u;
      const actualizado = { ...u, es_anfitrion: true };
      const ref = usuarios.find((x) => x.id === u.id);
      if (ref) ref.es_anfitrion = true;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(actualizado));
      return actualizado;
    });
  }, []);

  const value = useMemo<Sesion>(
    () => ({
      usuario,
      rol: usuario ? (usuario.es_anfitrion ? "anfitrion" : "huesped") : null,
      esAnfitrion: !!usuario?.es_anfitrion,
      cargando,
      login,
      logout,
      activarAnfitrion,
    }),
    [usuario, cargando, login, logout, activarAnfitrion],
  );

  return <SesionCtx.Provider value={value}>{children}</SesionCtx.Provider>;
}

export function useSesion(): Sesion {
  const ctx = useContext(SesionCtx);
  if (!ctx) throw new Error("useSesion debe usarse dentro de <SesionProvider>");
  return ctx;
}

/** Id del usuario logueado (string vacío si no hay sesión). */
export function useUsuarioId(): string {
  return useSesion().usuario?.id ?? "";
}
