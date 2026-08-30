import { Clock } from "lucide-react";
import { cn } from "@/lib/utils";
import { useSesion } from "@/lib/auth";
import { formatHoras } from "@/lib/millas";

/** Recuadro con el saldo de horas del usuario (al lado del nombre). */
export function HorasBadge({ className }: { className?: string }) {
  const { usuario, horas } = useSesion();
  if (!usuario) return null;
  return (
    <span
      title="Horas acumuladas: 100 horas = 1 de descuento"
      className={cn(
        "flex items-center gap-1.5 rounded-full border border-primary/30 bg-primary/10 px-2.5 py-1 text-xs font-semibold text-primary",
        className,
      )}
    >
      <Clock className="size-3.5" />
      {formatHoras(horas)} hs
    </span>
  );
}
