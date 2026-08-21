import { useState } from "react";
import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useSesion } from "@/lib/auth";
import { usuarios } from "@/lib/mock-data";

export const Route = createFileRoute("/login")({
  head: () => ({
    meta: [
      { title: "Iniciar sesión — estadía" },
      {
        name: "description",
        content: "Ingresá a tu cuenta de huésped o anfitrión para reservar y gestionar estadías.",
      },
      { property: "og:title", content: "Iniciar sesión — estadía" },
      { property: "og:description", content: "Accedé a tu cuenta de huésped o anfitrión." },
    ],
  }),
  component: Login,
});

function Login() {
  const { login, usuario, logout } = useSesion();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [cargando, setCargando] = useState(false);

  async function entrar(mail: string) {
    setCargando(true);
    try {
      const u = await login(mail);
      toast.success(`Hola, ${u.nombre}`);
      navigate({ to: u.es_anfitrion ? "/anfitrion" : "/" });
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setCargando(false);
    }
  }

  if (usuario) {
    return (
      <main className="mx-auto max-w-lg px-4 pb-20 pt-16 text-center">
        <h1 className="text-4xl">Ya iniciaste sesión</h1>
        <p className="mt-2 text-muted-foreground">
          {usuario.nombre} · {usuario.es_anfitrion ? "Anfitrión" : "Huésped"}
        </p>
        <div className="mt-6 flex justify-center gap-2">
          <Button asChild>
            <Link to="/">Ir a buscar</Link>
          </Button>
          <Button variant="outline" onClick={logout}>
            Cerrar sesión
          </Button>
        </div>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-lg px-4 pb-20 pt-12">
      <h1 className="text-4xl">Iniciar sesión</h1>
      <p className="mt-2 text-muted-foreground">
        Ingresá con tu email. Tu rol (huésped o anfitrión) define qué secciones ves.
      </p>

      <form
        className="surface-card mt-8 space-y-5 p-6"
        onSubmit={(e) => {
          e.preventDefault();
          void entrar(email);
        }}
      >
        <div className="space-y-1.5">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            required
            placeholder="tu@mail.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <Button type="submit" className="w-full" disabled={cargando}>
          Entrar
        </Button>
        <p className="text-center text-sm text-muted-foreground">
          ¿No tenés cuenta?{" "}
          <Link to="/registro" className="text-primary underline">
            Registrate
          </Link>
        </p>
      </form>

      <div className="surface-card mt-6 space-y-2 p-5">
        <p className="text-xs uppercase tracking-wide text-muted-foreground">Cuentas de prueba</p>
        {usuarios.map((u) => (
          <button
            key={u.id}
            onClick={() => void entrar(u.email)}
            className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-sm transition-colors hover:bg-secondary"
          >
            <span>
              {u.nombre} · <span className="text-muted-foreground">{u.email}</span>
            </span>
            <span className="text-xs text-muted-foreground">
              {u.es_anfitrion ? "Anfitrión" : "Huésped"}
            </span>
          </button>
        ))}
      </div>
    </main>
  );
}
