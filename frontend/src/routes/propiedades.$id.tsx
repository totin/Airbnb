import { lazy, Suspense, useEffect, useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { MapPin, Star, Users } from "lucide-react";
import { toast } from "sonner";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { money } from "@/components/property-card";
import {
  crearReserva,
  getDisponibilidad,
  getLugaresCercanosAPropiedad,
  getPropiedad,
  getResenasDePropiedad,
  noches,
} from "@/lib/api";
import { useSesion } from "@/lib/auth";
import { formatHoras, horasGanadas, horasParaPagar, HORAS_POR_DOLAR } from "@/lib/millas";
import { cn } from "@/lib/utils";

const MapaPropiedad = lazy(() =>
  import("@/components/mapa-propiedad").then((m) => ({ default: m.MapaPropiedad })),
);

export const Route = createFileRoute("/propiedades/$id")({
  head: () => ({
    meta: [
      { title: "Detalle de la propiedad — estadía" },
      {
        name: "description",
        content: "Fotos, amenidades, calendario de disponibilidad y reseñas de la propiedad.",
      },
      { property: "og:title", content: "Detalle de la propiedad — estadía" },
      {
        property: "og:description",
        content: "Disponibilidad, reseñas y reserva en línea.",
      },
    ],
  }),
  component: DetallePropiedad,
  errorComponent: ({ error }) => <p className="p-10 text-center">{error.message}</p>,
  notFoundComponent: () => <p className="p-10 text-center">Propiedad no encontrada.</p>,
});

function DetallePropiedad() {
  const { usuario, horas } = useSesion();
  const usuarioId = usuario?.id ?? "";
  const [medioPago, setMedioPago] = useState<"dinero" | "horas">("dinero");
  const { id } = Route.useParams();
  const qc = useQueryClient();
  const [mes, setMes] = useState(() => new Date().toISOString().slice(0, 7));
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [montado, setMontado] = useState(false);
  useEffect(() => setMontado(true), []);

  const { data: prop } = useQuery({ queryKey: ["propiedad", id], queryFn: () => getPropiedad(id) });
  const { data: resenas = [] } = useQuery({
    queryKey: ["resenas", id],
    queryFn: () => getResenasDePropiedad(id),
  });
  const { data: dias = [] } = useQuery({
    queryKey: ["disponibilidad", id, mes],
    queryFn: () => getDisponibilidad(id, mes),
  });
  const { data: lugaresCerca = [] } = useQuery({
    queryKey: ["lugares-propiedad", id],
    queryFn: () => getLugaresCercanosAPropiedad(id),
  });

  const reservar = useMutation({
    mutationFn: () => {
      if (!usuarioId) throw new Error("Iniciá sesión para reservar");
      return crearReserva({
        propiedad_id: id,
        huesped_id: usuarioId,
        fecha_inicio: desde,
        fecha_fin: hasta,
        metodo_pago: medioPago,
      });
    },
    onSuccess: () => {
      if (medioPago === "dinero") {
        toast.success(`Reserva pendiente · ganaste ${formatHoras(horasGanadas(totalDinero))} horas`);
      } else {
        toast.success(`Reserva pendiente · canjeaste ${formatHoras(horasParaPagar(totalDinero))} horas`);
      }
      qc.invalidateQueries({ queryKey: ["reservas"] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  if (!prop) return <p className="p-10 text-center text-muted-foreground">Cargando…</p>;

  const cantNoches = desde && hasta ? noches(desde, hasta) : 0;
  const totalDinero = prop.precio_noche * cantNoches;
  const costoHoras = horasParaPagar(totalDinero);
  const ganaHoras = horasGanadas(totalDinero);
  const alcanzan = cantNoches > 0 && horas >= costoHoras;

  return (
    <main className="mx-auto max-w-6xl px-4 pb-20 pt-8">
      <Link to="/" className="text-sm text-muted-foreground hover:text-foreground">
        ← Volver a la búsqueda
      </Link>

      <header className="mt-3">
        <h1 className="text-4xl">{prop.titulo}</h1>
        <p className="mt-2 flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
          <span className="flex items-center gap-1.5">
            <MapPin className="size-4" /> {prop.direccion}, {prop.ciudad}
          </span>
          <span className="flex items-center gap-1.5">
            <Users className="size-4" /> hasta {prop.capacidad} huéspedes
          </span>
          <span className="flex items-center gap-1.5">
            <Star className="size-4 fill-warning text-warning" />
            {prop.promedio_puntaje ? prop.promedio_puntaje.toFixed(1) : "sin reseñas"} (
            {prop.cantidad_resenas})
          </span>
          <span>Anfitrión: {prop.anfitrion?.nombre}</span>
        </p>
      </header>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_340px]">
        <div className="space-y-6">
          <div className="surface-card flex h-56 items-end p-6">
            <span className="font-display text-7xl text-primary/25">{prop.ciudad}</span>
          </div>

          <section className="surface-card p-5">
            <h2 className="text-xl">Amenidades</h2>
            <div className="mt-3 flex flex-wrap gap-2">
              {prop.amenidades_nombres.map((a) => (
                <Badge key={a} variant="secondary" className="font-normal">
                  {a}
                </Badge>
              ))}
            </div>
          </section>

          {prop.lat != null && prop.lng != null && (
            <section className="surface-card p-5">
              <h2 className="text-xl">Ubicación y qué hay cerca</h2>
              <p className="mt-1 text-sm text-muted-foreground">
                {prop.direccion}, {prop.ciudad}
              </p>
              <div className="mt-4 overflow-hidden rounded-lg">
                {montado ? (
                  <Suspense
                    fallback={<div className="h-64 animate-pulse rounded-lg bg-secondary" />}
                  >
                    <MapaPropiedad
                      lat={prop.lat}
                      lng={prop.lng}
                      titulo={prop.titulo}
                      lugares={lugaresCerca}
                    />
                  </Suspense>
                ) : (
                  <div className="h-64 rounded-lg bg-secondary" />
                )}
              </div>
              {lugaresCerca.length > 0 && (
                <ul className="mt-4 space-y-1.5 text-sm">
                  {lugaresCerca.slice(0, 5).map((l) => (
                    <li key={l.id} className="flex items-center justify-between gap-3">
                      <span className="flex items-center gap-1.5">
                        <MapPin className="size-3.5 text-primary" /> {l.nombre}
                      </span>
                      <span className="text-muted-foreground">a {l.distancia_km.toFixed(1)} km</span>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          )}

          <section className="surface-card p-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h2 className="text-xl">Disponibilidad</h2>
              <Input
                type="month"
                className="w-44"
                value={mes}
                onChange={(e) => setMes(e.target.value)}
              />
            </div>
            <div className="mt-4 grid grid-cols-7 gap-1.5">
              {dias.map((d) => (
                <div
                  key={d.fecha}
                  title={d.fecha}
                  className={
                    "flex h-10 items-center justify-center rounded-md text-sm " +
                    (d.ocupado
                      ? "bg-destructive/10 text-destructive line-through"
                      : "bg-success/10 text-success")
                  }
                >
                  {Number(d.fecha.slice(-2))}
                </div>
              ))}
            </div>
            <p className="mt-3 text-xs text-muted-foreground">
              Solo las reservas confirmadas ocupan fechas.
            </p>
          </section>

          <section className="surface-card p-5">
            <h2 className="text-xl">Reseñas ({resenas.length})</h2>
            <div className="mt-4 space-y-4">
              {resenas.length === 0 && (
                <p className="text-sm text-muted-foreground">Todavía no hay reseñas.</p>
              )}
              {resenas.map((r) => (
                <div key={r.id}>
                  <div className="flex items-center gap-2">
                    <span className="font-medium">{r.autor?.nombre}</span>
                    <span className="flex items-center gap-0.5 text-sm">
                      <Star className="size-3.5 fill-warning text-warning" /> {r.puntaje}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {new Date(r.fecha).toLocaleDateString("es-AR")}
                    </span>
                  </div>
                  <p className="mt-1 text-sm text-muted-foreground">{r.comentario}</p>
                  <Separator className="mt-4" />
                </div>
              ))}
            </div>
          </section>
        </div>

        <aside className="surface-card sticky top-24 h-fit space-y-4 p-5">
          <p className="text-2xl font-semibold">
            {money(prop.precio_noche)}
            <span className="text-sm font-normal text-muted-foreground"> / noche</span>
          </p>
          <div className="space-y-1.5">
            <Label className="text-xs uppercase text-muted-foreground">Check-in</Label>
            <Input type="date" value={desde} onChange={(e) => setDesde(e.target.value)} />
          </div>
          <div className="space-y-1.5">
            <Label className="text-xs uppercase text-muted-foreground">Check-out</Label>
            <Input type="date" value={hasta} onChange={(e) => setHasta(e.target.value)} />
          </div>
          <Separator />
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">
              {cantNoches} noche{cantNoches === 1 ? "" : "s"}
            </span>
            <span className="font-semibold">{money(totalDinero)}</span>
          </div>

          <div className="space-y-2">
            <Label className="text-xs uppercase text-muted-foreground">¿Cómo querés pagar?</Label>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setMedioPago("dinero")}
                className={cn(
                  "rounded-lg border p-3 text-left transition-colors",
                  medioPago === "dinero" ? "border-primary bg-primary/5" : "border-border",
                )}
              >
                <span className="block text-xs font-medium uppercase text-muted-foreground">
                  Con dinero
                </span>
                <span className="block text-sm font-semibold">{money(totalDinero)}</span>
                <span className="mt-1 block text-xs font-semibold text-success">
                  + {formatHoras(ganaHoras)} hs que ganás
                </span>
              </button>

              <button
                type="button"
                onClick={() => setMedioPago("horas")}
                className={cn(
                  "rounded-lg border p-3 text-left transition-colors",
                  medioPago === "horas" ? "border-primary bg-primary/5" : "border-border",
                )}
              >
                <span className="block text-xs font-medium uppercase text-muted-foreground">
                  Con horas
                </span>
                <span
                  className={cn(
                    "block text-sm font-semibold",
                    alcanzan ? "text-destructive" : "text-destructive/45",
                  )}
                >
                  {formatHoras(costoHoras)} hs
                </span>
                <span className="mt-1 block text-xs text-muted-foreground">
                  {cantNoches === 0
                    ? "Elegí las fechas"
                    : alcanzan
                      ? "Te alcanza"
                      : `Te faltan ${formatHoras(costoHoras - horas)} hs`}
                </span>
              </button>
            </div>
            <p className="text-xs text-muted-foreground">
              Ganás {HORAS_POR_DOLAR} horas por cada unidad gastada · 100 horas = 1 de descuento.
              Tu saldo: {formatHoras(horas)} hs.
            </p>
          </div>

          <Button
            className="w-full"
            disabled={
              !desde || !hasta || reservar.isPending || (medioPago === "horas" && !alcanzan)
            }
            onClick={() => reservar.mutate()}
          >
            {medioPago === "horas" ? `Reservar con ${formatHoras(costoHoras)} hs` : "Reservar"}
          </Button>
          <p className="text-xs text-muted-foreground">
            La reserva queda pendiente hasta que el anfitrión la confirme.
          </p>
        </aside>
      </div>
    </main>
  );
}