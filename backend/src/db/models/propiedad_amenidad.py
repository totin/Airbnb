from sqlalchemy import Column, Integer, ForeignKey
from src.db.connection import Base

class PropiedadAmenidad(Base):
    __tablename__ = "propiedad_amenidades"

    propiedad_id = Column(Integer, ForeignKey("propiedades.id"), primary_key=True)
    amenidad_id = Column(Integer, ForeignKey("amenidades.id"), primary_key=True)