from datetime import date
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from src.db.models.reserva import Reserva, EstadoReserva, MetodoPago
from src.db.models.propiedad import Propiedad
from src.db.models.usuario import Usuario
from src.db.models.resena import Resena
from src.db.models.transaccion_horas import TipoTransaccionHoras
from src.services.horas_service import HorasService
from src.services.propiedad_service import PropiedadService
from src.dtos.usuario_dto import UsuarioResponseDTO


class ReservaService:
    def __init__(self, db: Session):
        self.db = db
        self.horas_service = HorasService(db)

    def _calcular_noches(self, fecha_inicio: date, fecha_fin: date) -> int:
        if fecha_inicio >= fecha_fin:
            raise ValueError("La fecha de inicio debe ser anterior a la de fin")
        return (fecha_fin - fecha_inicio).days

    def _calcular_total(self, propiedad: Propiedad, fecha_inicio: date, fecha_fin: date) -> float:
        noches = self._calcular_noches(fecha_inicio, fecha_fin)
        return round(float(propiedad.precio_noche) * noches, 2)

    def enriquecer_reserva(self, reserva: Reserva) -> dict:
        prop = reserva.propiedad
        anfitrion_dto = None
        prop_data = None

        if prop:
            prop_service = PropiedadService(self.db)
            prop_data = prop_service.enriquecer_propiedad(prop)
            if prop.anfitrion:
                anfitrion_dto = UsuarioResponseDTO(
                    id=prop.anfitrion.id,
                    email=prop.anfitrion.email,
                    nombre=prop.anfitrion.nombre,
                    fecha_registro=prop.anfitrion.fecha_registro,
                    es_anfitrion=prop.anfitrion.es_anfitrion,
                )

        huesped_dto = None
        if reserva.huesped:
            huesped_dto = UsuarioResponseDTO(
                id=reserva.huesped.id,
                email=reserva.huesped.email,
                nombre=reserva.huesped.nombre,
                fecha_registro=reserva.huesped.fecha_registro,
                es_anfitrion=reserva.huesped.es_anfitrion,
            )

        tiene_resena = (
            self.db.query(Resena).filter(Resena.reserva_id == reserva.id).first() is not None
        )

        return {
            "id": reserva.id,
            "propiedad_id": reserva.propiedad_id,
            "huesped_id": reserva.huesped_id,
            "fecha_inicio": reserva.fecha_inicio,
            "fecha_fin": reserva.fecha_fin,
            "estado": reserva.estado,
            "total": float(reserva.total),
            "metodo_pago": reserva.metodo_pago,
            "horas_utilizadas": reserva.horas_utilizadas,
            "horas_ganadas": reserva.horas_ganadas,
            "propiedad": prop_data,
            "anfitrion": anfitrion_dto,
            "huesped": huesped_dto,
            "tiene_resena": tiene_resena,
        }

    def crear_reserva(
        self,
        propiedad_id: int,
        huesped_id: int,
        fecha_inicio: date,
        fecha_fin: date,
        metodo_pago: str = "dinero",
    ) -> dict:
        prop = self.db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
        if not prop:
            raise ValueError(f"No existe la propiedad con ID {propiedad_id}")

        if prop.anfitrion_id == huesped_id:
            raise ValueError("No podés reservar tu propia propiedad")

        if fecha_inicio >= fecha_fin:
            raise ValueError("La fecha de inicio debe ser anterior a la de fin")

        # Validar solapamiento con reservas confirmadas
        solapada = (
            self.db.query(Reserva)
            .filter(
                Reserva.propiedad_id == propiedad_id,
                Reserva.estado == "confirmada",
                Reserva.fecha_inicio < fecha_fin,
                Reserva.fecha_fin > fecha_inicio,
            )
            .first()
        )
        if solapada:
            raise ValueError("Ya existe una reserva confirmada en ese rango de fechas")

        total = self._calcular_total(prop, fecha_inicio, fecha_fin)

        horas_ganadas = None
        horas_utilizadas = None

        metodo_str = str(metodo_pago).lower()
        if metodo_str == "horas":
            horas_utilizadas = round(total * 100)
            # Valida saldo suficiente y descuenta antes de crear la reserva
            self.horas_service.restar_horas(
                usuario_id=huesped_id,
                cantidad=horas_utilizadas,
                reserva_id=None,
                tipo=TipoTransaccionHoras.GASTADA,
            )
        else:
            metodo_str = "dinero"
            horas_ganadas = round(total * 5)

        reserva = Reserva(
            propiedad_id=propiedad_id,
            huesped_id=huesped_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            total=Decimal(str(total)),
            estado="pendiente",
            metodo_pago=metodo_str,
            horas_ganadas=horas_ganadas,
            horas_utilizadas=horas_utilizadas,
        )
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)

        if metodo_str == "dinero" and horas_ganadas:
            self.horas_service.sumar_horas(
                usuario_id=huesped_id,
                cantidad=horas_ganadas,
                reserva_id=reserva.id,
                tipo=TipoTransaccionHoras.GANADA,
            )

        return self.enriquecer_reserva(reserva)

    def obtener_por_id(self, reserva_id: int) -> dict:
        reserva = self.db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if not reserva:
            raise ValueError(f"No existe la reserva con ID {reserva_id}")
        return self.enriquecer_reserva(reserva)

    def listar_por_huesped(self, huesped_id: int, estado: Optional[str] = None) -> list[dict]:
        query = self.db.query(Reserva).filter(Reserva.huesped_id == huesped_id)
        if estado and estado != "todos":
            query = query.filter(Reserva.estado == estado)
        query = query.order_by(Reserva.fecha_inicio.desc())
        return [self.enriquecer_reserva(r) for r in query.all()]

    def listar_por_anfitrion(self, anfitrion_id: int) -> list[dict]:
        query = (
            self.db.query(Reserva)
            .join(Propiedad, Reserva.propiedad_id == Propiedad.id)
            .filter(Propiedad.anfitrion_id == anfitrion_id)
            .order_by(Reserva.fecha_inicio.desc())
        )
        return [self.enriquecer_reserva(r) for r in query.all()]

    def cambiar_estado_reserva(
        self,
        reserva_id: int,
        nuevo_estado: str,
        actor_id: Optional[int] = None,
    ) -> dict:
        reserva = self.db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if not reserva:
            raise ValueError(f"No existe la reserva con ID {reserva_id}")

        validas = {
            "pendiente": ["confirmada", "rechazada", "cancelada"],
            "confirmada": ["cancelada", "finalizada"],
            "rechazada": [],
            "cancelada": [],
            "finalizada": [],
        }

        if nuevo_estado not in validas.get(reserva.estado, []):
            raise ValueError(f"Transición inválida: {reserva.estado} → {nuevo_estado}")

        if actor_id:
            prop = reserva.propiedad
            es_duenio = prop and prop.anfitrion_id == actor_id
            es_huesped = reserva.huesped_id == actor_id

            if (nuevo_estado == "confirmada" or nuevo_estado == "rechazada") and not es_duenio:
                raise ValueError("Solo el anfitrión dueño puede confirmar o rechazar la reserva")

            if nuevo_estado == "cancelada" and not (es_duenio or es_huesped):
                raise ValueError("No tenés permiso para cancelar esta reserva")

        # Gestión de horas al cancelar / rechazar
        if nuevo_estado in ["cancelada", "rechazada"]:
            if reserva.metodo_pago == "horas" and reserva.horas_utilizadas:
                self.horas_service.sumar_horas(
                    usuario_id=reserva.huesped_id,
                    cantidad=reserva.horas_utilizadas,
                    reserva_id=reserva.id,
                    tipo=TipoTransaccionHoras.DEVUELTA,
                )
            elif reserva.metodo_pago == "dinero" and reserva.horas_ganadas:
                try:
                    self.horas_service.restar_horas(
                        usuario_id=reserva.huesped_id,
                        cantidad=reserva.horas_ganadas,
                        reserva_id=reserva.id,
                        tipo=TipoTransaccionHoras.AJUSTE,
                    )
                except ValueError:
                    pass  # Si ya no tiene saldo para restar, continuar

        reserva.estado = nuevo_estado
        self.db.commit()
        self.db.refresh(reserva)
        return self.enriquecer_reserva(reserva)

    def cancelar_reserva(self, reserva_id: int, usuario_id: int) -> dict:
        return self.cambiar_estado_reserva(reserva_id, "cancelada", actor_id=usuario_id)