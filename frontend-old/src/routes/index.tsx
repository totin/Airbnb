import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Search } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { PropertyCard } from "@/components/property-card";
import {
  agregarFavorito,
  buscarPropiedades,
  getAmenidades,
  getFavoritos,
  quitarFavorito,
} from "@/lib/api";
import { useUsuarioId } from "@/lib/auth";
import type { FiltrosBusqueda } from "@/lib/types";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Buscar alojamientos por ciudad y fechas — estadía" },
      {
        name: "description",
        content:
          "Filtrá alquileres temporarios por ciudad, fechas, huéspedes, precio máximo y amenidades.",
      },
      { property: "og:title", content: "Buscar alojamientos — estadía" },
      {
        property: "og:description",
        content: "Filtrá por ciudad, fechas, huéspedes, precio y amenidades.",
      },
    ],
  }),
  component: Buscar,
});

function Buscar() {
  const usuarioId = useUsuarioId();
  const qc = useQueryClient();
  const [filtros, setFiltros] = useState<FiltrosBusqueda>({});
  const [aplicados, setAplicados] = useState<FiltrosBusqueda>({});

  const { data: amenidades = [] } = useQuery({ queryKey: ["amenidades"], queryFn: getAmenidades });
  const { data: resultados = [], isFetching } = useQuery({
    queryKey: ["propiedades", aplicados],
    queryFn: () => buscarPropiedades(aplicados),
  });
  const { data: favoritos = [] } = useQuery({
    queryKey: ["favoritos", usuarioId],
    queryFn: () => getFavoritos(usuarioId),
    enabled: !!usuarioId,
  });

  const toggleFav = useMutation({
    mutationFn: async (propiedadId: string) => {
      if (!usuarioId) throw new Error("Iniciá sesión para guardar favoritos");
      const esFav = favoritos.some((f) => f.id === propiedadId);
      return esFav
        ? quitarFavorito(usuarioId, propiedadId)
        : agregarFavorito(usuarioId, propiedadId);
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["favoritos", usuarioId] }),
    onError: (e: Error) => toast.error(e.message),
  });

  const seleccionadas = filtros.amenidades ?? [];
  const toggleAmenidad = (id: string) =>
    setFiltros((f) => ({
      ...f,
      amenidades: seleccionadas.includes(id)
        ? seleccionadas.filter((a) => a !== id)
        : [...seleccionadas, id],
    }));

  return (
    <main className="mx-auto max-w-6xl px-4 pb-20">
      <section className="py-12 text-center">
        <h1 className="text-balance text-5xl md:text-6xl">
          Encontrá tu próxima <em className="text-primary">estadía</em>
        </h1>
        <p className="mx-auto mt-3 max-w-xl text-muted-foreground">
          Buscá por ciudad y fechas, mirá la disponibilidad real y reservá en dos pasos.
        </p>
      </section>

      <form
        className="surface-card grid gap-4 p-5 md:grid-cols-5"
        onSubmit={(e) => {
          e.preventDefault();
          setAplicados(filtros);
        }}
      >
        <Field label="Ciudad">
          <Input
            placeholder="Bariloche"
            value={filtros.ciudad ?? ""}
            onChange={(e) => setFiltros((f) => ({ ...f, ciudad: e.target.value }))}
          />
        </Field>
        <Field label="Desde">
          <Input
            type="date"
            value={filtros.desde ?? ""}
            onChange={(e) => setFiltros((f) => ({ ...f, desde: e.target.value }))}
          />
        </Field>
        <Field label="Hasta">
          <Input
            type="date"
            value={filtros.hasta ?? ""}
            onChange={(e) => setFiltros((f) => ({ ...f, hasta: e.target.value }))}
          />
        </Field>
        <Field label="Huéspedes">
          <Input
            type="number"
            min={1}
            value={filtros.huespedes ?? ""}
            onChange={(e) =>
              setFiltros((f) => ({ ...f, huespedes: Number(e.target.value) || undefined }))
            }
          />
        </Field>
        <Field label="Precio máx. / noche">
          <Input
            type="number"
            min={0}
            value={filtros.precio_max ?? ""}
            onChange={(e) =>
              setFiltros((f) => ({ ...f, precio_max: Number(e.target.value) || undefined }))
            }
          />
        </Field>

        <div className="md:col-span-5">
          <Label className="mb-2 block text-xs uppercase tracking-wide text-muted-foreground">
            Amenidades (deben cumplirse todas)
          </Label>
          <div className="flex flex-wrap gap-2">
            {amenidades.map((a) => (
              <button key={a.id} type="button" onClick={() => toggleAmenidad(a.id)}>
                <Badge
                  variant={seleccionadas.includes(a.id) ? "default" : "outline"}
                  className="cursor-pointer px-3 py-1 font-normal"
                >
                  {a.nombre}
                </Badge>
              </button>
            ))}
          </div>
        </div>

        <div className="flex gap-2 md:col-span-5">
          <Button type="submit">
            <Search className="size-4" /> Buscar
          </Button>
          <Button
            type="button"
            variant="ghost"
            onClick={() => {
              setFiltros({});
              setAplicados({});
            }}
          >
            Limpiar
          </Button>
        </div>
      </form>

      <div className="mt-8 flex items-baseline justify-between">
        <h2 className="text-2xl">
          {isFetching ? "Buscando…" : `${resultados.length} propiedades`}
        </h2>
      </div>

      <div className="mt-4 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {resultados.map((p) => (
          <PropertyCard
            key={p.id}
            propiedad={p}
            esFavorito={favoritos.some((f) => f.id === p.id)}
            onToggleFavorito={(id) => toggleFav.mutate(id)}
          />
        ))}
      </div>
      {!isFetching && resultados.length === 0 && (
        <p className="mt-10 text-center text-muted-foreground">
          No hay propiedades disponibles con esos filtros.
        </p>
      )}
    </main>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-1.5">
      <Label className="text-xs uppercase tracking-wide text-muted-foreground">{label}</Label>
      {children}
    </div>
  );
}
