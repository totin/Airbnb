import { Link } from "@tanstack/react-router";
import { Heart, MapPin, Star, Users } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
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
  return (
    <article className="surface-card group flex flex-col overflow-hidden transition-transform hover:-translate-y-0.5">
      {/* Cabecera con Imagen / Fallback */}
      <div className="relative flex h-48 items-end bg-secondary p-4 overflow-hidden">
        {propiedad.imagen_url ? (
          <img
            src={propiedad.imagen_url}
            alt={propiedad.titulo}
            className="absolute inset-0 h-full w-full object-cover transition-transform group-hover:scale-105"
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
            className="absolute right-3 top-3 rounded-full z-10 bg-background/80 backdrop-blur-sm hover:bg-background"
          >
            <Heart className={cn("size-4", esFavorito && "fill-primary text-primary")} />
          </Button>
        )}
      </div>

      <div className="flex flex-1 flex-col gap-2 p-4">
        <div className="flex items-start justify-between gap-3">
          <h3 className="text-lg leading-tight font-medium">
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