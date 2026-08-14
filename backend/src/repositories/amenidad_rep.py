from sqlalchemy.orm import Session
from models.amenidad import Amenidad
from models.propiedad import Propiedad


class AmenidadRepository:

    def __init__(self, db: Session):
        self.db = db

    def crear(self, amenidad: Amenidad) -> Amenidad:
        self.db.add(amenidad)
        self.db.commit()
        self.db.refresh(amenidad)
        return amenidad

    def obtener_por_id(
        self,
        amenidad_id: int
    ) -> Amenidad | None:

        return (
            self.db.query(Amenidad)
            .filter(Amenidad.id == amenidad_id)
            .first()
        )

    def obtener_por_nombre(
        self,
        nombre: str
    ) -> Amenidad | None:

        return (
            self.db.query(Amenidad)
            .filter(Amenidad.nombre == nombre)
            .first()
        )

    def obtener_todas(self) -> list[Amenidad]:
        return self.db.query(Amenidad).all()

    def obtener_propiedades_con_amenidades(
        self,
        amenidades: list[str]
    ) -> list[Propiedad]:

        query = self.db.query(Propiedad)

        for nombre in amenidades:
            query = query.filter(
                Propiedad.amenidades.any(
                    Amenidad.nombre == nombre
                )
            )

        return query.all()