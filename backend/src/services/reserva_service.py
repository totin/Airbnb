from src.db.models.reserva import Reserva, EstadoReserva, MetodoPago
from src.db.models.transaccion_horas import TipoTransaccionHoras
from src.services.horas_service import HorasService


class ReservaService:
    def __init__(self, db):
        self.db = db
        self.horas_service = HorasService(db)

    def crear_reserva(self, propiedad_id, huesped_id, fecha_inicio, fecha_fin, metodo_pago=MetodoPago.DINERO):
        # ... acá va tu lógica actual de calcular `total` según noches y precio_noche ...
        total = self._calcular_total(propiedad_id, fecha_inicio, fecha_fin)  # el método que ya tengas

        horas_ganadas = None
        horas_utilizadas = None

        if metodo_pago == MetodoPago.DINERO:
            horas_ganadas = round(float(total) * 5)
        else:  # HORAS
            horas_utilizadas = round(float(total) * 100)
            # valida saldo suficiente y descuenta ANTES de confirmar la reserva
            self.horas_service.restar_horas(
                usuario_id=huesped_id,
                cantidad=horas_utilizadas,
                reserva_id=None,  # se completa después de crear la reserva
                tipo=TipoTransaccionHoras.GASTADA,
            )

        reserva = Reserva(
            propiedad_id=propiedad_id,
            huesped_id=huesped_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            total=total,
            metodo_pago=metodo_pago,
            horas_ganadas=horas_ganadas,
            horas_utilizadas=horas_utilizadas,
        )
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)

        if metodo_pago == MetodoPago.DINERO:
            self.horas_service.sumar_horas(
                usuario_id=huesped_id,
                cantidad=horas_ganadas,
                reserva_id=reserva.id,
                tipo=TipoTransaccionHoras.GANADA,
            )

        return reserva

    def cancelar_reserva(self, reserva_id: int, usuario_id: int):
        reserva = self.db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if not reserva:
            raise ValueError(f"No existe la reserva con ID {reserva_id}")
        # ... tu validación actual de permisos/estado ...

        reserva.estado = EstadoReserva.CANCELADA

        if reserva.metodo_pago == MetodoPago.HORAS and reserva.horas_utilizadas:
            self.horas_service.sumar_horas(
                usuario_id=reserva.huesped_id,
                cantidad=reserva.horas_utilizadas,
                reserva_id=reserva.id,
                tipo=TipoTransaccionHoras.DEVUELTA,
            )
        elif reserva.metodo_pago == MetodoPago.DINERO and reserva.horas_ganadas:
            self.horas_service.restar_horas(
                usuario_id=reserva.huesped_id,
                cantidad=reserva.horas_ganadas,
                reserva_id=reserva.id,
                tipo=TipoTransaccionHoras.AJUSTE,
            )

        self.db.commit()
        self.db.refresh(reserva)
        return reserva