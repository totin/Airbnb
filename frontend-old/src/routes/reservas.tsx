import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { money } from "@/components/property-card";
import { estadoVariant } from "@/components/estado-badge";
import {
  calcularPenalidad,
  cambiarEstadoReserva,
  crearResena,
  getReservasDeUsuario,
} from "@/lib/api";
import { useUsuarioId } from "@/lib/auth";
import { RequireAuth } from "@/components/require-auth";
import type { EstadoReserva, ReservaConDatos } from "@/lib/types";

export const Route = createFileRoute("/reservas")({
  head: () => ({
    meta: [
      { title: "Mis reservas — estadía" },
      {
        name: "description",
        content: "Historial de reservas con estado, propiedad, anfitrión y reseñas post-estadía.",
      },
      { property: "og:title", content: "Mis reservas — estadía" },
      { property: "og:description", content: "Historial completo de tus estadías." },
    ],
  }),
  component: () => (
    <RequireAuth>
      <Reservas />
    </RequireAuth>
  ),
});

const ESTADOS: EstadoReserva[] = ["pendiente", "confirmada", "rechazada", "cancelada"];

function Reservas() {
  const usuarioId = useUsuarioId();
  const qc = useQueryClient();
  const [estado, setEstado] = useState<string>("todos");
  const [resenando, setResenando] = useState<ReservaConDatos | null>(null);
  const [puntaje, setPuntaje] = useState(5);
  const [comentario, setComentario] = useState("");

  const { data: reservas = [] } = useQuery({
    queryKey: ["reservas", usuarioId, estado],
    queryFn: () =>
      getReservasDeUsuario(
        usuarioId,
        estado === "todos" ? undefined : (estado as EstadoReserva),
      ),
  });

  const invalidar = () => qc.invalidateQueries({ queryKey: ["reservas"] });

  const cancelar = useMutation({
    mutationFn: (id: string) => cambiarEstadoReserva(id, "cancelada", usuarioId),
    onSuccess: () => {
      toast.success("Reserva cancelada");
      invalidar();
    },
    onError: (e: Error) => toast.error(e.message),
  });

  const resenar = useMutation({
    mutationFn: () =>
      crearResena({
        reserva_id: resenando!.id,
        autor_id: usuarioId,
        puntaje,
        comentario,
      }),
    onSuccess: () => {
      toast.success("¡Gracias por tu reseña!");
      setResenando(null);
      setComentario("");
      invalidar();
      qc.invalidateQueries({ queryKey: ["resenas"] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  const hoy = new Date();

  return (
    <main className="mx-auto max-w-4xl px-4 pb-20 pt-10">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-4xl">Mis reservas</h1>
          <p className="mt-2 text-muted-foreground">Ordenadas por fecha de inicio descendente.</p>
        </div>
        <Select value={estado} onValueChange={setEstado}>
          <SelectTrigger className="w-48">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="todos">Todos los estados</SelectItem>
            {ESTADOS.map((e) => (
              <SelectItem key={e} value={e}>
                {e}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="mt-8 space-y-4">
        {reservas.map((r) => {
          const penalidad = calcularPenalidad(r, hoy);
          const puedeResenar =
            r.estado === "confirmada" && new Date(r.fecha_fin) < hoy && !r.tiene_resena;
          return (
            <article key={r.id} className="surface-card flex flex-wrap gap-4 p-5">
              <div className="min-w-56 flex-1">
                <div className="flex items-center gap-2">
                  <h2 className="text-xl">{r.propiedad?.titulo}</h2>
                  <Badge variant={estadoVariant(r.estado)}>{r.estado}</Badge>
                </div>
                <p className="mt-1 text-sm text-muted-foreground">
                  {r.propiedad?.ciudad} · Anfitrión: {r.anfitrion?.nombre}
                </p>
                <p className="mt-1 text-sm text-muted-foreground">
                  {r.fecha_inicio} → {r.fecha_fin}
                </p>
              </div>
              <div className="flex flex-col items-end justify-between gap-2">
                <p className="text-lg font-semibold">{money(r.total)}</p>
                <div className="flex gap-2">
                  {puedeResenar && (
                    <Button size="sm" variant="outline" onClick={() => setResenando(r)}>
                      Dejar reseña
                    </Button>
                  )}
                  {r.estado === "confirmada" && new Date(r.fecha_inicio) > hoy && (
                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() => cancelar.mutate(r.id)}
                      title={`Penalidad estimada: ${money(penalidad)}`}
                    >
                      Cancelar
                    </Button>
                  )}
                </div>
                {r.estado === "confirmada" && new Date(r.fecha_inicio) > hoy && penalidad > 0 && (
                  <p className="text-xs text-destructive">
                    Penalidad si cancelás hoy: {money(penalidad)}
                  </p>
                )}
              </div>
            </article>
          );
        })}
        {reservas.length === 0 && <p className="text-muted-foreground">No hay reservas.</p>}
      </div>

      <Dialog open={Boolean(resenando)} onOpenChange={(o) => !o && setResenando(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Reseñar «{resenando?.propiedad?.titulo}»</DialogTitle>
          </DialogHeader>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map((n) => (
              <Button
                key={n}
                type="button"
                size="sm"
                variant={puntaje === n ? "default" : "outline"}
                onClick={() => setPuntaje(n)}
              >
                {n}
              </Button>
            ))}
          </div>
          <Textarea
            placeholder="¿Cómo fue tu estadía?"
            value={comentario}
            onChange={(e) => setComentario(e.target.value)}
          />
          <DialogFooter>
            <Button onClick={() => resenar.mutate()} disabled={resenar.isPending}>
              Publicar reseña
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </main>
  );
}