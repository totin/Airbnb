import { Link } from "@tanstack/react-router";
import { Heart, MapPin, Star, Users } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useSesion } from "@/lib/auth";
import { formatHoras, horasParaPagar } from "@/lib/millas";
import type { PropiedadConDatos } from "@/lib/types";

export const money = (n: number) =>
  new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS", maximumFractionDigits: 0 }).format(n);

export function PropertyCard({
  propiedad,
  esFavorito,
  onToggleFavorito,
}: {
  propiedad: PropiedadConDatos;
  esFavorito?: boolean;
  onToggleFavorito?: (id: string) => void;
}) {
  const { horas } = useSesion();
  const costoHoras = horasParaPagar(propiedad.precio_noche);
  const alcanza = horas >= costoHoras;

  return (
    <article className="surface-card group flex flex-col overflow-hidden transition-transform hover:-translate-y-0.5">
      <div className="relative flex h-36 items-end overflow-hidden bg-secondary p-4">
        {propiedad.imagenes?.[0] ? (
          <img
            src={propiedad.imagenes[0]}
            alt={`Foto de ${propiedad.titulo}`}
            loading="lazy"
            className="absolute inset-0 size-full object-cover"
          />
        ) : (
          <span className="font-display text-5xl text-primary/25">{propiedad.ciudad.slice(0, 2)}</span>
        )}
        {onToggleFavorito && (
          <Button
            size="icon"
            variant="secondary"
            aria-label={esFavorito ? "Quitar de favoritos" : "Agregar a favoritos"}
            onClick={() => onToggleFavorito(propiedad.id)}
            className="absolute right-3 top-3 rounded-full"
          >
            <Heart className={cn("size-4", esFavorito && "fill-primary text-primary")} />
          </Button>
        )}
      </div>

      <div className="flex flex-1 flex-col gap-2 p-4">
        <div className="flex items-start justify-between gap-3">
          <h3 className="text-lg leading-tight">
            <Link to="/propiedades/$id" params={{ id: propiedad.id }} className="hover:text-primary">
              {propiedad.titulo}
            </Link>
          </h3>
          <span className="flex shrink-0 items-center gap-1 text-sm">
            <Star className="size-3.5 fill-warning text-warning" />
            {propiedad.promedio_puntaje ? propiedad.promedio_puntaje.toFixed(1) : "—"}
            <span className="text-muted-foreground">({propiedad.cantidad_resenas})</span>
          </span>
        </div>

        <p className="flex items-center gap-1.5 text-sm text-muted-foreground">
          <MapPin className="size-3.5" /> {propiedad.ciudad} · {propiedad.direccion}
        </p>
        <p className="flex items-center gap-1.5 text-sm text-muted-foreground">
          <Users className="size-3.5" /> hasta {propiedad.capacidad} huéspedes
        </p>

        <div className="flex flex-wrap gap-1.5 pt-1">
          {propiedad.amenidades_nombres.slice(0, 3).map((a) => (
            <Badge key={a} variant="secondary" className="font-normal">
              {a}
            </Badge>
          ))}
          {propiedad.amenidades_nombres.length > 3 && (
            <Badge variant="outline" className="font-normal">
              +{propiedad.amenidades_nombres.length - 3}
            </Badge>
          )}
        </div>

        <div className="mt-auto flex items-end justify-between pt-3">
          <p className="text-base font-semibold">
            {money(propiedad.precio_noche)}
            <span className="text-sm font-normal text-muted-foreground"> / noche</span>
            <span
              title={
                alcanza
                  ? "Te alcanzan las horas para una noche"
                  : "No te alcanzan las horas para una noche"
              }
              className={cn(
                "block text-xs font-semibold",
                alcanza ? "text-destructive" : "text-destructive/45",
              )}
            >
              o {formatHoras(costoHoras)} hs
            </span>
          </p>
          <Button asChild size="sm">
            <Link to="/propiedades/$id" params={{ id: propiedad.id }}>
              Ver
            </Link>
          </Button>
        </div>
      </div>
    </article>
  );
}