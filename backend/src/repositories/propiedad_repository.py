from sqlalchemy.orm import Session
from sqlalchemy import and_, not_, exists
from src.db.models.propiedad import Propiedad
from src.db.models.reserva import Reserva



class PropiedadRepository:

    def __init__(self, db: Session):
        self.db = db

    def crear(self, propiedad: Propiedad) -> Propiedad:
        self.db.add(propiedad)
        self.db.commit()
        self.db.refresh(propiedad)
        return propiedad

    def obtener_por_id(self, propiedad_id: int) -> Propiedad | None:
        return (
            self.db.query(Propiedad)
            .filter(Propiedad.id == propiedad_id)
            .first()
        )

    def obtener_por_anfitrion(self, anfitrion_id: int) -> list[Propiedad]:
        return (
            self.db.query(Propiedad)
            .filter(Propiedad.anfitrion_id == anfitrion_id)
            .all()
        )

    def buscar_por_ciudad(
        self,
        ciudad: str,
        huespedes: int | None = None,
        precio_max: float | None = None
    ) -> list[Propiedad]:

        query = self.db.query(Propiedad).filter(
            Propiedad.ciudad == ciudad
        )

        if huespedes is not None:
            query = query.filter(
                Propiedad.capacidad >= huespedes
            )

        if precio_max is not None:
            query = query.filter(
                Propiedad.precio_noche <= precio_max
            )

        return query.all()

    def buscar_disponibles(
        self,
        ciudad: str,
        fecha_inicio,
        fecha_fin,
        huespedes: int | None = None,
        precio_max: float | None = None
    ) -> list[Propiedad]:

        query = self.db.query(Propiedad).filter(
            Propiedad.ciudad == ciudad
        )

        if huespedes is not None:
            query = query.filter(
                Propiedad.capacidad >= huespedes
            )

        if precio_max is not None:
            query = query.filter(
                Propiedad.precio_noche <= precio_max
            )

        reservas_solapadas = exists().where(
            and_(
                Reserva.propiedad_id == Propiedad.id,
                Reserva.estado == "confirmada",
                Reserva.fecha_inicio < fecha_fin,
                Reserva.fecha_fin > fecha_inicio
            )
        )

        query = query.filter(not_(reservas_solapadas))

        return query.all()

    def actualizar(self, propiedad: Propiedad) -> Propiedad:
        self.db.commit()
        self.db.refresh(propiedad)
        return propiedad

    def eliminar(self, propiedad: Propiedad) -> None:
        self.db.delete(propiedad)
        self.db.commit()