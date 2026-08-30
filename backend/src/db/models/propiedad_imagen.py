from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from src.db.connection import Base


class PropiedadImagen(Base):
    __tablename__ = "propiedad_imagenes"

    id = Column(Integer, primary_key=True, index=True)
    propiedad_id = Column(Integer, ForeignKey("propiedad.id", ondelete="CASCADE"), nullable=False)
    url = Column(Text, nullable=False)
    orden = Column(Integer, default=0, nullable=False)
    es_portada = Column(Boolean, default=False, nullable=False)