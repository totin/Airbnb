from sqlalchemy.orm import Session
from src.db.models.amenidad import Amenidad
from src.db.models.propiedad import Propiedad


class AmenidadRepository:

    def __init__(self, db: Session):
        self.db = db

    def crear(self, amenidad: Amenidad) -> Amenidad:
        self.db.add(amenidad)
        self.db.commit()
        self.db.refresh(amenidad)
        return amenidad

    def create(self, nombre: str) -> Amenidad:
        return self.crear(Amenidad(nombre=nombre))

    def obtener_por_id(
        self,
        amenidad_id: int
    ) -> Amenidad | None:

        return (
            self.db.query(Amenidad)
            .filter(Amenidad.id == amenidad_id)
            .first()
        )

    def get_by_id(self, amenidad_id: int) -> Amenidad | None:
        return self.obtener_por_id(amenidad_id)

    def obtener_por_nombre(
        self,
        nombre: str
    ) -> Amenidad | None:

        return (
            self.db.query(Amenidad)
            .filter(Amenidad.nombre == nombre)
            .first()
        )

    def get_by_nombre(self, nombre: str) -> Amenidad | None:
        return self.obtener_por_nombre(nombre)

    def obtener_todas(self) -> list[Amenidad]:
        return self.db.query(Amenidad).all()

    def get_all(self) -> list[Amenidad]:
        return self.obtener_todas()

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