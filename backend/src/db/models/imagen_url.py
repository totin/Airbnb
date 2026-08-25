from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from src.db.connection import Base

class Propiedad(Base):
    __tablename__ = "propiedades"

    id = Column(Integer, primary_key=True, index=True)
    # ... tus campos actuales ...
    imagen_url = Column(String(500), nullable=True)  # <--- Agregá esta línea