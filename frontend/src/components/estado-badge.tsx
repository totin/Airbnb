import type { EstadoReserva } from "@/lib/types";

export function estadoVariant(
  estado: EstadoReserva,
): "default" | "secondary" | "destructive" | "outline" {
  switch (estado) {
    case "confirmada":
      return "default";
    case "pendiente":
      return "secondary";
    case "rechazada":
    case "cancelada":
      return "destructive";
    default:
      return "outline";
  }
}