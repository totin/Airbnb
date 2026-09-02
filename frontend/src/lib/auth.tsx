import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import {
  getUsuarioPorEmail,
  getSaldoHoras,
  sumarHorasApi,
  gastarHorasApi,
  activarAnfitrionApi,
} from "./api";
import type { Usuario } from "./types";

export type Rol = "huesped" | "anfitrion";

interface Sesion {
  usuario: Usuario | null;
  rol: Rol | null;
  esAnfitrion: boolean;
  cargando: boolean;
  login: (email: string) => Promise<Usuario>;
  logout: () => void;
  activarAnfitrion: () => Promise<void>;
  horas: number;
  sumarHoras: (cantidad: number) => Promise<void>;
  gastarHoras: (cantidad: number) => Promise<boolean>;
  recargarSaldo: () => Promise<void>;
}

const STORAGE_KEY = "estadia.sesion";
const SesionCtx = createContext<Sesion | null>(null);

export function SesionProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [cargando, setCargando] = useState(true);
  const [horas, setHoras] = useState(0);

  const sincronizarSaldo = useCallback(async (usuarioId: string) => {
    try {
      const saldo = await getSaldoHoras(usuarioId);
      setHoras(saldo);
    } catch {
      /* ignore */
    }
  }, []);

  useEffect(() => {
    async function inicializar() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
          const u = JSON.parse(raw) as Usuario;
          setUsuario(u);
          await sincronizarSaldo(u.id);
        }
      } catch {
        /* noop */
      } finally {
        setCargando(false);
      }
    }
    void inicializar();
  }, [sincronizarSaldo]);

  const login = useCallback(
    async (email: string) => {
      const u = await getUsuarioPorEmail(email.trim());
      setUsuario(u);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(u));
      await sincronizarSaldo(u.id);
      return u;
    },
    [sincronizarSaldo]
  );

  const logout = useCallback(() => {
    setUsuario(null);
    setHoras(0);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  const activarAnfitrion = useCallback(async () => {
    if (!usuario) return;
    const actualizado = await activarAnfitrionApi(usuario.id);
    setUsuario(actualizado);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(actualizado));
  }, [usuario]);

  const sumarHoras = useCallback(
    async (cantidad: number) => {
      if (!usuario) return;
      const cant = Math.max(0, Math.round(cantidad));
      const nuevoSaldo = await sumarHorasApi(usuario.id, cant);
      setHoras(nuevoSaldo);
    },
    [usuario]
  );

  const gastarHoras = useCallback(
    async (cantidad: number) => {
      if (!usuario) return false;
      const costo = Math.max(0, Math.round(cantidad));
      if (costo > horas) return false;
      const nuevoSaldo = await gastarHorasApi(usuario.id, costo);
      setHoras(nuevoSaldo);
      return true;
    },
    [usuario, horas]
  );

  const recargarSaldo = useCallback(async () => {
    if (usuario) {
      await sincronizarSaldo(usuario.id);
    }
  }, [usuario, sincronizarSaldo]);

  const value = useMemo<Sesion>(
    () => ({
      usuario,
      rol: usuario ? (usuario.es_anfitrion ? "anfitrion" : "huesped") : null,
      esAnfitrion: !!usuario?.es_anfitrion,
      cargando,
      login,
      logout,
      activarAnfitrion,
      horas,
      sumarHoras,
      gastarHoras,
      recargarSaldo,
    }),
    [usuario, cargando, login, logout, activarAnfitrion, horas, sumarHoras, gastarHoras, recargarSaldo]
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

