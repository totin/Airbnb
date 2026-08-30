import { useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { money } from "@/components/property-card";
import { estadoVariant } from "@/components/estado-badge";
import {
  cambiarEstadoReserva,
  getIngresos,
  getPropiedadesDeAnfitrion,
  getReservasDeAnfitrion,
} from "@/lib/api";
import { useUsuarioId } from "@/lib/auth";
import { RequireAuth } from "@/components/require-auth";

export const Route = createFileRoute("/anfitrion")({
  head: () => ({
    meta: [
      { title: "Panel de anfitrión — estadía" },
      {
        name: "description",
        content: "Publicá propiedades, gestioná reservas recibidas y consultá tus ingresos.",
      },
      { property: "og:title", content: "Panel de anfitrión — estadía" },
      { property: "og:description", content: "Publicaciones, reservas e ingresos en un lugar." },
    ],
  }),
  component: () => (
    <RequireAuth soloAnfitrion>
      <Anfitrion />
    </RequireAuth>
  ),
});

function Anfitrion() {
  return (
    <main className="mx-auto max-w-5xl px-4 pb-20 pt-10">
      <h1 className="text-4xl">Panel de anfitrión</h1>
      <p className="mt-2 text-muted-foreground">
        Publicaciones, reservas recibidas e ingresos facturados.
      </p>

      <Tabs defaultValue="propiedades" className="mt-8">
        <TabsList>
          <TabsTrigger value="propiedades">Mis propiedades</TabsTrigger>
          <TabsTrigger value="reservas">Reservas recibidas</TabsTrigger>
          <TabsTrigger value="ingresos">Ingresos</TabsTrigger>
        </TabsList>
        <TabsContent value="propiedades" className="mt-6">
          <Propiedades />
        </TabsContent>
        <TabsContent value="reservas" className="mt-6">
          <ReservasRecibidas />
        </TabsContent>
        <TabsContent value="ingresos" className="mt-6">
          <Ingresos />
        </TabsContent>
      </Tabs>
    </main>
  );
}

function Propiedades() {
  const usuarioId = useUsuarioId();
  const { data: props = [] } = useQuery({
    queryKey: ["propiedades-anfitrion", usuarioId],
    queryFn: () => getPropiedadesDeAnfitrion(usuarioId),
  });



  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
      <div className="space-y-3">
        {props.map((p) => (
          <div key={p.id} className="surface-card flex items-center justify-between gap-4 p-4">
            <div>
              <h3 className="text-lg">{p.titulo}</h3>
              <p className="text-sm text-muted-foreground">
                {p.ciudad} · {p.capacidad} huéspedes · {p.cantidad_resenas} reseñas
              </p>
            </div>
            <p className="font-semibold">{money(p.precio_noche)}</p>
          </div>
        ))}
        {props.length === 0 && <p className="text-muted-foreground">Todavía no publicaste nada.</p>}
      </div>

      <Link
        to="/publicar"
        className="surface-card flex h-fit flex-col gap-2 p-5 transition-colors hover:bg-secondary"
      >
        <h2 className="text-xl">Publicar propiedad</h2>
        <p className="text-sm text-muted-foreground">
          Cargá una casa, departamento u hotel desde la solapa Publicar.
        </p>
        <span className="text-sm font-medium text-primary">Ir a publicar →</span>
      </Link>
    </div>
  );
}

function ReservasRecibidas() {
  const usuarioId = useUsuarioId();
  const qc = useQueryClient();
  const { data: reservas = [] } = useQuery({
    queryKey: ["reservas-anfitrion", usuarioId],
    queryFn: () => getReservasDeAnfitrion(usuarioId),
  });

  const cambiar = useMutation({
    mutationFn: (v: { id: string; estado: "confirmada" | "rechazada" | "cancelada" }) =>
      cambiarEstadoReserva(v.id, v.estado, usuarioId),
    onSuccess: () => {
      toast.success("Estado actualizado");
      qc.invalidateQueries({ queryKey: ["reservas-anfitrion"] });
      qc.invalidateQueries({ queryKey: ["reservas"] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  return (
    <div className="space-y-3">
      {reservas.map((r) => (
        <div key={r.id} className="surface-card flex flex-wrap items-center gap-4 p-4">
          <div className="min-w-56 flex-1">
            <div className="flex items-center gap-2">
              <h3 className="text-lg">{r.propiedad?.titulo}</h3>
              <Badge variant={estadoVariant(r.estado)}>{r.estado}</Badge>
            </div>
            <p className="text-sm text-muted-foreground">
              {r.huesped?.nombre} · {r.fecha_inicio} → {r.fecha_fin}
            </p>
          </div>
          <p className="font-semibold">{money(r.total)}</p>
          <div className="flex gap-2">
            {r.estado === "pendiente" && (
              <>
                <Button
                  size="sm"
                  onClick={() => cambiar.mutate({ id: r.id, estado: "confirmada" })}
                >
                  Confirmar
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => cambiar.mutate({ id: r.id, estado: "rechazada" })}
                >
                  Rechazar
                </Button>
              </>
            )}
            {r.estado === "confirmada" && (
              <Button
                size="sm"
                variant="destructive"
                onClick={() => cambiar.mutate({ id: r.id, estado: "cancelada" })}
              >
                Cancelar
              </Button>
            )}
          </div>
        </div>
      ))}
      {reservas.length === 0 && <p className="text-muted-foreground">Sin reservas recibidas.</p>}
    </div>
  );
}

function Ingresos() {
  const usuarioId = useUsuarioId();
  const [desde, setDesde] = useState("2026-01-01");
  const [hasta, setHasta] = useState("2026-12-31");
  const { data } = useQuery({
    queryKey: ["ingresos", usuarioId, desde, hasta],
    queryFn: () => getIngresos(usuarioId, desde, hasta),
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-4">
        <div className="space-y-1.5">
          <Label className="text-xs uppercase text-muted-foreground">Desde</Label>
          <Input type="date" value={desde} onChange={(e) => setDesde(e.target.value)} />
        </div>
        <div className="space-y-1.5">
          <Label className="text-xs uppercase text-muted-foreground">Hasta</Label>
          <Input type="date" value={hasta} onChange={(e) => setHasta(e.target.value)} />
        </div>
      </div>

      <div className="surface-card p-6">
        <p className="text-sm uppercase tracking-wide text-muted-foreground">Total facturado</p>
        <p className="font-display text-5xl text-primary">{money(data?.total ?? 0)}</p>
        <p className="mt-1 text-xs text-muted-foreground">
          Solo reservas confirmadas con fecha de fin dentro del rango.
        </p>
      </div>

      <div className="space-y-3">
        {data?.detalle.map((d) => (
          <div key={d.propiedad_id} className="surface-card flex justify-between gap-4 p-4">
            <div>
              <h3 className="text-lg">{d.titulo}</h3>
              <p className="text-sm text-muted-foreground">{d.reservas} reservas</p>
            </div>
            <p className="font-semibold">{money(d.total)}</p>
          </div>
        ))}
      </div>
    </div>
  );
}