from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.db.connection import Base

class Favorito(Base):
    __tablename__ = "favoritos"

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    propiedad_id = Column(Integer, ForeignKey("propiedades.id"), primary_key=True)

    fecha = Column(DateTime, server_default=func.now())