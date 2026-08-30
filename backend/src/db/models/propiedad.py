from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from src.db.connection import Base


class Propiedad(Base):
    __tablename__ = "propiedad"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    direccion = Column(String(200), nullable=False)
    ciudad = Column(String(100), nullable=False)
    precio_noche = Column(Numeric(10, 2), nullable=False)
    capacidad = Column(Integer, nullable=False)
    anfitrion_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)

    imagenes = relationship(
        "PropiedadImagen",
        cascade="all, delete-orphan",
        order_by="PropiedadImagen.orden"
    )