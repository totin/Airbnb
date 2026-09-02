from sqlalchemy import Column, Integer, ForeignKey
from src.db.connection import Base


class PropiedadAmenidad(Base):
    __tablename__ = "propiedad_amenidades"

    propiedad_id = Column(Integer, ForeignKey("propiedad.id", ondelete="CASCADE"), primary_key=True)
    amenidad_id = Column(Integer, ForeignKey("amenidad.id", ondelete="CASCADE"), primary_key=True)