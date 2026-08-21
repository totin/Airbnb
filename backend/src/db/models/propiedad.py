from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.db.connection import Base

class Propiedad(Base):
    __tablename__ = "propiedades"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    direccion = Column(String(200), nullable=False)
    ciudad = Column(String(100), nullable=False)
    precio_noche = Column(Float, nullable=False)
    capacidad = Column(Integer, nullable=False)

    anfitrion_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)