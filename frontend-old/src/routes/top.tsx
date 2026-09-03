import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { PropertyCard } from "@/components/property-card";
import { getTopPropiedades } from "@/lib/api";

export const Route = createFileRoute("/top")({
  head: () => ({
    meta: [
      { title: "Top propiedades por ciudad — estadía" },
      {
        name: "description",
        content: "Las 10 propiedades mejor calificadas de cada ciudad, con al menos 3 reseñas.",
      },
      { property: "og:title", content: "Top propiedades por ciudad — estadía" },
      { property: "og:description", content: "Ranking por promedio de puntaje." },
    ],
  }),
  component: Top,
});

function Top() {
  const [ciudad, setCiudad] = useState("");
  const { data = [] } = useQuery({
    queryKey: ["top", ciudad],
    queryFn: () => getTopPropiedades(ciudad || undefined),
  });

  return (
    <main className="mx-auto max-w-6xl px-4 pb-20 pt-10">
      <h1 className="text-4xl">Mejor calificadas</h1>
      <p className="mt-2 text-muted-foreground">
        Top 10 por promedio de puntaje. Solo propiedades con 3 reseñas o más.
      </p>

      <div className="mt-6 max-w-xs space-y-1.5">
        <Label className="text-xs uppercase text-muted-foreground">Ciudad</Label>
        <Input
          placeholder="Todas"
          value={ciudad}
          onChange={(e) => setCiudad(e.target.value)}
        />
      </div>

      <ol className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {data.map((p, i) => (
          <li key={p.id} className="relative">
            <span className="absolute -left-1 -top-3 z-10 flex size-8 items-center justify-center rounded-full bg-primary font-display text-lg text-primary-foreground">
              {i + 1}
            </span>
            <PropertyCard propiedad={p} />
          </li>
        ))}
      </ol>
      {data.length === 0 && (
        <p className="mt-10 text-muted-foreground">
          No hay propiedades con al menos 3 reseñas para esa ciudad.
        </p>
      )}
    </main>
  );
}