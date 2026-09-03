import { useEffect, useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { Pencil, Trash2 } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { money } from "@/components/property-card";
import { estadoVariant } from "@/components/estado-badge";
import { ImageDropzone } from "@/components/image-dropzone";
import {
  actualizarPropiedad,
  cambiarEstadoReserva,
  eliminarPropiedad,
  getAmenidades,
  getIngresos,
  getPropiedadesDeAnfitrion,
  getReservasDeAnfitrion,
} from "@/lib/api";
import type { PropiedadConDatos } from "@/lib/types";
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
  const qc = useQueryClient();
  const { data: props = [] } = useQuery({
    queryKey: ["propiedades-anfitrion", usuarioId],
    queryFn: () => getPropiedadesDeAnfitrion(usuarioId),
  });

  const [editando, setEditando] = useState<PropiedadConDatos | null>(null);

  const invalidar = () => {
    qc.invalidateQueries({ queryKey: ["propiedades-anfitrion"] });
    qc.invalidateQueries({ queryKey: ["propiedades"] });
    qc.invalidateQueries({ queryKey: ["top"] });
  };

  const borrar = useMutation({
    // DELETE /propiedades/{id}
    mutationFn: (id: string) => eliminarPropiedad(id, usuarioId),
    onSuccess: () => {
      toast.success("Publicación eliminada");
      invalidar();
    },
    onError: (e: Error) => toast.error(e.message),
  });

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
      <div className="space-y-3">
        {props.map((p) => (
          <div key={p.id} className="surface-card flex flex-wrap items-center gap-4 p-4">
            {p.imagenes?.[0] && (
              <img
                src={p.imagenes[0]}
                alt={`Foto de ${p.titulo}`}
                loading="lazy"
                className="size-16 rounded-md object-cover"
              />
            )}
            <div className="min-w-48 flex-1">
              <h3 className="text-lg">{p.titulo}</h3>
              <p className="text-sm text-muted-foreground">
                {p.ciudad} · {p.capacidad} huéspedes · {p.cantidad_resenas} reseñas
              </p>
            </div>
            <p className="font-semibold">{money(p.precio_noche)}</p>
            <div className="flex gap-2">
              <Button size="sm" variant="outline" onClick={() => setEditando(p)}>
                <Pencil className="size-4" />
                Editar
              </Button>
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button size="sm" variant="destructive">
                    <Trash2 className="size-4" />
                    Borrar
                  </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>¿Borrar “{p.titulo}”?</AlertDialogTitle>
                    <AlertDialogDescription>
                      Se eliminará la publicación y sus favoritos. No se puede deshacer.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Cancelar</AlertDialogCancel>
                    <AlertDialogAction onClick={() => borrar.mutate(p.id)}>Borrar</AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          </div>
        ))}
        {props.length === 0 && <p className="text-muted-foreground">Todavía no publicaste nada.</p>}
      </div>

      <DialogEditar
        propiedad={editando}
        usuarioId={usuarioId}
        onClose={() => setEditando(null)}
        onSaved={invalidar}
      />

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

function DialogEditar({
  propiedad,
  usuarioId,
  onClose,
  onSaved,
}: {
  propiedad: PropiedadConDatos | null;
  usuarioId: string;
  onClose: () => void;
  onSaved: () => void;
}) {
  const { data: amenidades = [] } = useQuery({ queryKey: ["amenidades"], queryFn: getAmenidades });
  const [form, setForm] = useState({
    titulo: "",
    ciudad: "",
    direccion: "",
    precio_noche: "",
    capacidad: "",
  });
  const [sel, setSel] = useState<string[]>([]);
  const [imagenes, setImagenes] = useState<string[]>([]);

  useEffect(() => {
    if (!propiedad) return;
    setForm({
      titulo: propiedad.titulo,
      ciudad: propiedad.ciudad,
      direccion: propiedad.direccion,
      precio_noche: String(propiedad.precio_noche),
      capacidad: String(propiedad.capacidad),
    });
    setSel(propiedad.amenidades);
    setImagenes(propiedad.imagenes ?? []);
  }, [propiedad]);

  const guardar = useMutation({
    // PUT /propiedades/{id}
    mutationFn: () =>
      actualizarPropiedad(propiedad!.id, usuarioId, {
        titulo: form.titulo,
        ciudad: form.ciudad,
        direccion: form.direccion,
        precio_noche: Number(form.precio_noche),
        capacidad: Number(form.capacidad),
        amenidades: sel,
        imagenes,
      }),
    onSuccess: () => {
      toast.success("Publicación actualizada");
      onSaved();
      onClose();
    },
    onError: (e: Error) => toast.error(e.message),
  });

  return (
    <Dialog open={!!propiedad} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-h-[85vh] overflow-y-auto sm:max-w-2xl">
        <DialogHeader>
          <DialogTitle>Editar publicación</DialogTitle>
        </DialogHeader>
        <form
          className="space-y-4"
          onSubmit={(e) => {
            e.preventDefault();
            guardar.mutate();
          }}
        >
          <div className="grid gap-4 sm:grid-cols-2">
            {(
              [
                ["titulo", "Título", "text"],
                ["ciudad", "Ciudad", "text"],
                ["direccion", "Dirección", "text"],
                ["precio_noche", "Precio por noche", "number"],
                ["capacidad", "Capacidad (huéspedes)", "number"],
              ] as const
            ).map(([key, label, type]) => (
              <div key={key} className="space-y-1.5">
                <Label htmlFor={`edit-${key}`}>{label}</Label>
                <Input
                  id={`edit-${key}`}
                  type={type}
                  required
                  min={type === "number" ? 1 : undefined}
                  value={form[key]}
                  onChange={(e) => setForm((f) => ({ ...f, [key]: e.target.value }))}
                />
              </div>
            ))}
          </div>

          <div className="space-y-2">
            <Label className="text-xs uppercase text-muted-foreground">Fotos</Label>
            <ImageDropzone imagenes={imagenes} onChange={setImagenes} />
          </div>

          <div className="space-y-2">
            <Label className="text-xs uppercase text-muted-foreground">Amenidades</Label>
            <div className="flex flex-wrap gap-2">
              {amenidades.map((a) => (
                <button
                  key={a.id}
                  type="button"
                  onClick={() =>
                    setSel((s) => (s.includes(a.id) ? s.filter((x) => x !== a.id) : [...s, a.id]))
                  }
                >
                  <Badge
                    variant={sel.includes(a.id) ? "default" : "outline"}
                    className="cursor-pointer font-normal"
                  >
                    {a.nombre}
                  </Badge>
                </button>
              ))}
            </div>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit" disabled={guardar.isPending}>
              Guardar cambios
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
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