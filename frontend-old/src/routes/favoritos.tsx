import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

import { PropertyCard } from "@/components/property-card";
import { getFavoritos, quitarFavorito } from "@/lib/api";
import { useUsuarioId } from "@/lib/auth";
import { RequireAuth } from "@/components/require-auth";

export const Route = createFileRoute("/favoritos")({
  head: () => ({
    meta: [
      { title: "Mis favoritos — estadía" },
      { name: "description", content: "Las propiedades que guardaste para reservar más adelante." },
      { property: "og:title", content: "Mis favoritos — estadía" },
      { property: "og:description", content: "Propiedades guardadas para reservar más adelante." },
    ],
  }),
  component: () => (
    <RequireAuth>
      <Favoritos />
    </RequireAuth>
  ),
});

function Favoritos() {
  const usuarioId = useUsuarioId();
  const qc = useQueryClient();
  const { data: favoritos = [], isLoading } = useQuery({
    queryKey: ["favoritos", usuarioId],
    queryFn: () => getFavoritos(usuarioId),
  });

  const quitar = useMutation({
    mutationFn: (id: string) => quitarFavorito(usuarioId, id),
    onSuccess: () => {
      toast.success("Quitado de favoritos");
      qc.invalidateQueries({ queryKey: ["favoritos", usuarioId] });
    },
  });

  return (
    <main className="mx-auto max-w-6xl px-4 pb-20 pt-10">
      <h1 className="text-4xl">Favoritos</h1>
      <p className="mt-2 text-muted-foreground">Propiedades guardadas por vos.</p>

      <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {favoritos.map((p) => (
          <PropertyCard
            key={p.id}
            propiedad={p}
            esFavorito
            onToggleFavorito={(id) => quitar.mutate(id)}
          />
        ))}
      </div>
      {!isLoading && favoritos.length === 0 && (
        <p className="mt-10 text-muted-foreground">Todavía no guardaste ninguna propiedad.</p>
      )}
    </main>
  );
}