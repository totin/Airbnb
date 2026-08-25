from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from src.db.connection import Base

class Propiedad(Base):
    __tablename__ = "propiedades"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Float, nullable=False)
    ubicacion = Column(String(200), nullable=True)
    imagen_url = Column(String(500), nullable=True)
    anfitrion_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)