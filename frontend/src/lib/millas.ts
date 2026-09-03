/**
 * Programa de fidelidad "Horas" (estilo millas aéreas).
 *
 * Reglas:
 *  - Se ganan 5 horas por cada dólar/peso gastado cuando se paga con dinero.
 *  - Cada hora equivale a 0,01 al momento de pagar (100 horas = 1).
 *    Ej: un gasto de 400 se paga con 40.000 horas, o se ganan 2.000 horas.
 *
 * Endpoints sugeridos (a implementar en el backend):
 *  - GET   /usuarios/{id}/horas                    -> { saldo }
 *  - POST  /usuarios/{id}/horas/acreditar { reserva_id }
 *  - POST  /reservas  { ..., medio_pago: "horas" | "dinero" }
 */

/** Horas ganadas por cada unidad de dinero gastada. */
export const HORAS_POR_DOLAR = 5;
/** Valor en dinero de una hora al canjearla. */
export const VALOR_HORA = 0.01;
/** Saldo inicial de horas para cuentas nuevas (mock). */
export const HORAS_INICIALES = 25_000;

/** Horas necesarias para pagar un gasto (gasto / 0.01). */
export const horasParaPagar = (monto: number) => Math.round(monto / VALOR_HORA);

/** Horas que se ganan si el gasto se paga con dinero. */
export const horasGanadas = (monto: number) => Math.round(monto * HORAS_POR_DOLAR);

export const formatHoras = (n: number) => new Intl.NumberFormat("es-AR").format(Math.round(n));
