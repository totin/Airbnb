import { useState } from "react";
import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { BadgeCheck, LogIn } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { money } from "@/components/property-card";
import { crearPropiedad, getAmenidades, getPropiedadesDeAnfitrion } from "@/lib/api";
import { useSesion } from "@/lib/auth";

export const Route = createFileRoute("/publicar")({
  head: () => ({
    meta: [
      { title: "Publicá tu casa o departamento — estadía" },
      {
        name: "description",
        content:
          "Publicá tu casa, departamento u hotel en estadía: cargá título, ciudad, precio por noche, capacidad y amenidades.",
      },
      { property: "og:title", content: "Publicá tu casa o departamento — estadía" },
      {
        property: "og:description",
        content: "Cargá tu propiedad en minutos y empezá a recibir reservas.",
      },
    ],
  }),
  component: PublicarPage,
});

function PublicarPage() {
  const { usuario, esAnfitrion, activarAnfitrion } = useSesion();

  return (
    <main className="mx-auto max-w-5xl px-4 pb-20 pt-10">
      <h1 className="text-4xl">Publicá tu espacio</h1>
      <p className="mt-2 text-muted-foreground">
        Casa, departamento, cabaña u hotel: cargalo una vez y recibí reservas de huéspedes.
      </p>

      {!usuario ? (
        <div className="surface-card mt-8 space-y-3 p-6">
          <h2 className="text-xl">Iniciá sesión para publicar</h2>
          <p className="text-sm text-muted-foreground">
            Necesitás una cuenta para cargar una propiedad y gestionar sus reservas.
          </p>
          <div className="flex gap-2">
            <Button asChild>
              <Link to="/login">
                <LogIn className="size-4" />
                Iniciar sesión
              </Link>
            </Button>
            <Button variant="outline" asChild>
              <Link to="/registro">Crear cuenta</Link>
            </Button>
          </div>
        </div>
      ) : !esAnfitrion ? (
        <div className="surface-card mt-8 space-y-3 p-6">
          <h2 className="text-xl">Convertite en anfitrión</h2>
          <p className="text-sm text-muted-foreground">
            Tu cuenta es de huésped. Activá el modo anfitrión para publicar propiedades y ver el
            panel de reservas e ingresos.
          </p>
          <Button
            onClick={() => {
              activarAnfitrion();
              toast.success("¡Listo! Ya sos anfitrión");
            }}
          >
            <BadgeCheck className="size-4" />
            Quiero ser anfitrión
          </Button>
        </div>
      ) : (
        <FormularioPublicacion usuarioId={usuario.id} />
      )}
    </main>
  );
}

function FormularioPublicacion({ usuarioId }: { usuarioId: string }) {
  const qc = useQueryClient();
  const navigate = useNavigate();
  const { data: amenidades = [] } = useQuery({ queryKey: ["amenidades"], queryFn: getAmenidades });
  const { data: props = [] } = useQuery({
    queryKey: ["propiedades-anfitrion", usuarioId],
    queryFn: () => getPropiedadesDeAnfitrion(usuarioId),
  });

  const [form, setForm] = useState({
    titulo: "",
    direccion: "",
    ciudad: "",
    precio_noche: "",
    capacidad: "",
  });
  const [sel, setSel] = useState<string[]>([]);

  const crear = useMutation({
    // POST /propiedades
    mutationFn: () =>
      crearPropiedad({
        titulo: form.titulo,
        direccion: form.direccion,
        ciudad: form.ciudad,
        precio_noche: Number(form.precio_noche),
        capacidad: Number(form.capacidad),
        anfitrion_id: usuarioId,
        amenidades: sel,
      }),
    onSuccess: () => {
      toast.success("Propiedad publicada");
      setForm({ titulo: "", direccion: "", ciudad: "", precio_noche: "", capacidad: "" });
      setSel([]);
      qc.invalidateQueries({ queryKey: ["propiedades-anfitrion"] });
      qc.invalidateQueries({ queryKey: ["propiedades"] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  return (
    <div className="mt-8 grid gap-6 lg:grid-cols-[minmax(0,1fr)_360px]">
      <form
        className="surface-card h-fit space-y-4 p-6"
        onSubmit={(e) => {
          e.preventDefault();
          crear.mutate();
        }}
      >
        <h2 className="text-xl">Datos de la propiedad</h2>
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
              <Label htmlFor={key}>{label}</Label>
              <Input
                id={key}
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
        <div className="flex flex-wrap gap-2">
          <Button type="submit" disabled={crear.isPending}>
            Publicar
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate({ to: "/anfitrion" })}
          >
            Ir al panel de anfitrión
          </Button>
        </div>
      </form>

      <aside className="space-y-3">
        <h2 className="text-xl">Tus publicaciones</h2>
        {props.map((p) => (
          <Link
            key={p.id}
            to="/propiedades/$id"
            params={{ id: p.id }}
            className="surface-card block p-4 transition-colors hover:bg-secondary"
          >
            <h3 className="text-lg">{p.titulo}</h3>
            <p className="text-sm text-muted-foreground">
              {p.ciudad} · {p.capacidad} huéspedes · {money(p.precio_noche)}
            </p>
          </Link>
        ))}
        {props.length === 0 && (
          <p className="text-sm text-muted-foreground">Todavía no publicaste ninguna propiedad.</p>
        )}
      </aside>
    </div>
  );
}
