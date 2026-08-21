from sqlalchemy.orm import Session
from src.db.models.propiedad_amenidad import PropiedadAmenidad


class PropiedadAmenidadRepository:

    def __init__(self, db: Session):
        self.db = db

    def existe_relacion(self, propiedad_id: int, amenidad_id: int) -> bool:
        return self.db.query(PropiedadAmenidad).filter(
            PropiedadAmenidad.propiedad_id == propiedad_id,
            PropiedadAmenidad.amenidad_id == amenidad_id
        ).first() is not None

    def get_relacion(self, propiedad_id: int, amenidad_id: int) -> PropiedadAmenidad | None:
        return self.db.query(PropiedadAmenidad).filter(
            PropiedadAmenidad.propiedad_id == propiedad_id,
            PropiedadAmenidad.amenidad_id == amenidad_id
        ).first()

    def create(self, propiedad_id: int, amenidad_id: int) -> PropiedadAmenidad:
        relacion = PropiedadAmenidad(propiedad_id=propiedad_id, amenidad_id=amenidad_id)
        self.db.add(relacion)
        self.db.commit()
        self.db.refresh(relacion)
        return relacion

    def delete(self, relacion: PropiedadAmenidad):
        self.db.delete(relacion)
        self.db.commit()
        return relacion