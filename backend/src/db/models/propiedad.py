from sqlalchemy import Column, Integer, String, Numeric, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.db.connection import Base


class Propiedad(Base):
    __tablename__ = "propiedad"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(150), nullable=False)
    direccion = Column(String(200), nullable=False)
    ciudad = Column(String(100), nullable=False, index=True)
    precio_noche = Column(Numeric(10, 2), nullable=False)
    capacidad = Column(Integer, nullable=False)
    anfitrion_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)

    anfitrion = relationship("Usuario", back_populates="propiedades")
    imagenes = relationship(
        "PropiedadImagen",
        cascade="all, delete-orphan",
        order_by="PropiedadImagen.orden",
        back_populates="propiedad",
    )
    amenidades = relationship(
        "Amenidad",
        secondary="propiedad_amenidades",
        back_populates="propiedades",
    )
    reservas = relationship("Reserva", back_populates="propiedad", cascade="all, delete-orphan")