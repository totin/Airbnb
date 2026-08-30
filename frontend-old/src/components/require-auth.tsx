import type { ReactNode } from "react";
import { Link } from "@tanstack/react-router";
import { LockKeyhole } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useSesion } from "@/lib/auth";

/** Gate por sesión y (opcionalmente) por rol de anfitrión. */
export function RequireAuth({
  children,
  soloAnfitrion = false,
}: {
  children: ReactNode;
  soloAnfitrion?: boolean;
}) {
  const { usuario, esAnfitrion, cargando } = useSesion();

  if (cargando) return <div className="mx-auto max-w-5xl px-4 py-20 text-muted-foreground">Cargando…</div>;

  if (!usuario) {
    return (
      <Aviso
        titulo="Necesitás iniciar sesión"
        texto="Ingresá con tu cuenta para ver esta sección."
        accion={{ to: "/login", label: "Ir a iniciar sesión" }}
      />
    );
  }

  if (soloAnfitrion && !esAnfitrion) {
    return (
      <Aviso
        titulo="Sección solo para anfitriones"
        texto="Tu cuenta está registrada como huésped. Creá una cuenta de anfitrión para publicar propiedades."
        accion={{ to: "/registro", label: "Crear cuenta de anfitrión" }}
      />
    );
  }

  return <>{children}</>;
}

function Aviso({
  titulo,
  texto,
  accion,
}: {
  titulo: string;
  texto: string;
  accion: { to: "/login" | "/registro"; label: string };
}) {
  return (
    <main className="mx-auto max-w-md px-4 py-24 text-center">
      <LockKeyhole className="mx-auto size-8 text-muted-foreground" />
      <h1 className="mt-4 text-3xl">{titulo}</h1>
      <p className="mt-2 text-muted-foreground">{texto}</p>
      <Button asChild className="mt-6">
        <Link to={accion.to}>{accion.label}</Link>
      </Button>
    </main>
  );
}
