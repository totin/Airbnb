from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.db.models.reserva import Reserva


class ReservaRepository:

    def __init__(self, db: Session):
        self.db = db

    def crear(self, reserva: Reserva) -> Reserva:
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def obtener_por_id(self, reserva_id: int) -> Reserva | None:
        return (
            self.db.query(Reserva)
            .filter(Reserva.id == reserva_id)
            .first()
        )

    def obtener_por_huesped(
        self,
        huesped_id: int,
        estado: str | None = None
    ) -> list[Reserva]:

        query = self.db.query(Reserva).filter(
            Reserva.huesped_id == huesped_id
        )

        if estado is not None:
            query = query.filter(
                Reserva.estado == estado
            )

        return (
            query
            .order_by(Reserva.fecha_inicio.desc())
            .all()
        )

    def obtener_por_propiedad(
        self,
        propiedad_id: int
    ) -> list[Reserva]:

        return (
            self.db.query(Reserva)
            .filter(Reserva.propiedad_id == propiedad_id)
            .all()
        )

    def obtener_confirmadas_por_propiedad(
        self,
        propiedad_id: int
    ) -> list[Reserva]:

        return (
            self.db.query(Reserva)
            .filter(
                Reserva.propiedad_id == propiedad_id,
                Reserva.estado == "confirmada"
            )
            .all()
        )

    def existe_solapamiento(
        self,
        propiedad_id: int,
        fecha_inicio,
        fecha_fin
    ) -> bool:

        reserva = (
            self.db.query(Reserva)
            .filter(
                Reserva.propiedad_id == propiedad_id,
                Reserva.estado == "confirmada",
                Reserva.fecha_inicio < fecha_fin,
                Reserva.fecha_fin > fecha_inicio
            )
            .first()
        )

        return reserva is not None

    def actualizar(self, reserva: Reserva) -> Reserva:
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def eliminar(self, reserva: Reserva) -> None:
        self.db.delete(reserva)
        self.db.commit()