import { Link, useNavigate } from "@tanstack/react-router";
import {
  Heart,
  CalendarDays,
  Home,
  Star,
  Building2,
  PlusSquare,
  LogIn,
  LogOut,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { useSesion } from "@/lib/auth";
import { HorasBadge } from "@/components/horas-badge";

const navPublico = [
  { to: "/", label: "Buscar", icon: Home },
  { to: "/top", label: "Top", icon: Star },
  { to: "/publicar", label: "Publicar", icon: PlusSquare },
] as const;

const navHuesped = [
  { to: "/favoritos", label: "Favoritos", icon: Heart },
  { to: "/reservas", label: "Mis reservas", icon: CalendarDays },
] as const;

const navAnfitrion = [{ to: "/anfitrion", label: "Anfitrión", icon: Building2 }] as const;

const linkClass =
  "flex items-center gap-1.5 rounded-full px-3 py-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground";

export function SiteHeader() {
  const { usuario, esAnfitrion, logout } = useSesion();
  const navigate = useNavigate();

  const items = [
    ...navPublico,
    ...(usuario ? navHuesped : []),
    ...(esAnfitrion ? navAnfitrion : []),
  ];

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/85 backdrop-blur">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-x-6 gap-y-2 px-4 py-3">
        <Link to="/" className="font-display text-2xl leading-none text-primary">
          estadía
        </Link>
        <nav className="flex flex-wrap items-center gap-1 text-sm">
          {items.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              activeOptions={{ exact: to === "/" }}
              className={linkClass}
              activeProps={{ className: "bg-secondary text-foreground font-medium" }}
            >
              <Icon className="size-4" />
              {label}
            </Link>
          ))}
        </nav>

        <div className="ml-auto flex items-center gap-2 text-sm">
          {usuario ? (
            <>
              <span className="hidden text-muted-foreground sm:inline">
                {usuario.nombre} ·{" "}
                <span className="text-foreground">{esAnfitrion ? "Anfitrión" : "Huésped"}</span>
              </span>
              <HorasBadge />
              <Button
                size="sm"
                variant="outline"
                onClick={() => {
                  logout();
                  navigate({ to: "/" });
                }}
              >
                <LogOut className="size-4" />
                Salir
              </Button>
            </>
          ) : (
            <>
              <Button size="sm" variant="ghost" asChild>
                <Link to="/registro">Registrarme</Link>
              </Button>
              <Button size="sm" asChild>
                <Link to="/login">
                  <LogIn className="size-4" />
                  Iniciar sesión
                </Link>
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
