from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.connection import Base


class Favorito(Base):
    __tablename__ = "favoritos"

    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), primary_key=True)
    propiedad_id = Column(Integer, ForeignKey("propiedad.id", ondelete="CASCADE"), primary_key=True)
    fecha = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="favoritos")
    propiedad = relationship("Propiedad")