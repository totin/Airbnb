import { useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { crearUsuario } from "@/lib/api";
import type { Usuario } from "@/lib/types";

export const Route = createFileRoute("/registro")({
  head: () => ({
    meta: [
      { title: "Crear cuenta — estadía" },
      {
        name: "description",
        content: "Registrate con tu email para reservar estadías o publicar propiedades.",
      },
      { property: "og:title", content: "Crear cuenta — estadía" },
      { property: "og:description", content: "Registrate para reservar o publicar propiedades." },
    ],
  }),
  component: Registro,
});

function Registro() {
  const [nombre, setNombre] = useState("");
  const [email, setEmail] = useState("");
  const [esAnfitrion, setEsAnfitrion] = useState(false);
  const [creado, setCreado] = useState<Usuario | null>(null);

  const registrar = useMutation({
    mutationFn: () => crearUsuario({ nombre, email, es_anfitrion: esAnfitrion }),
    onSuccess: (u) => {
      setCreado(u);
      toast.success("Usuario creado (201)");
      setNombre("");
      setEmail("");
    },
    onError: (e: Error) => toast.error(e.message),
  });

  return (
    <main className="mx-auto max-w-lg px-4 pb-20 pt-12">
      <h1 className="text-4xl">Crear cuenta</h1>
      <p className="mt-2 text-muted-foreground">
        El email es único. La fecha de registro se guarda automáticamente.
      </p>

      <form
        className="surface-card mt-8 space-y-5 p-6"
        onSubmit={(e) => {
          e.preventDefault();
          registrar.mutate();
        }}
      >
        <div className="space-y-1.5">
          <Label htmlFor="nombre">Nombre</Label>
          <Input id="nombre" required value={nombre} onChange={(e) => setNombre(e.target.value)} />
        </div>
        <div className="space-y-1.5">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="flex items-center justify-between rounded-lg bg-secondary px-4 py-3">
          <div>
            <Label htmlFor="anfitrion">Quiero publicar propiedades</Label>
            <p className="text-xs text-muted-foreground">es_anfitrion (por defecto false)</p>
          </div>
          <Switch id="anfitrion" checked={esAnfitrion} onCheckedChange={setEsAnfitrion} />
        </div>
        <Button type="submit" className="w-full" disabled={registrar.isPending}>
          Registrarme
        </Button>
        <p className="text-center text-sm text-muted-foreground">
          ¿Ya tenés cuenta?{" "}
          <Link to="/login" className="text-primary underline">
            Iniciá sesión
          </Link>
        </p>
      </form>

      {creado && (
        <pre className="surface-card mt-6 overflow-x-auto p-4 text-xs text-muted-foreground">
          {JSON.stringify(creado, null, 2)}
        </pre>
      )}
    </main>
  );
}