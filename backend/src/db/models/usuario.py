from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.connection import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(150), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    fecha_registro = Column(DateTime, server_default=func.now())
    es_anfitrion = Column(Boolean, default=False, nullable=False)

    propiedades = relationship("Propiedad", back_populates="anfitrion", cascade="all, delete-orphan")
    reservas = relationship("Reserva", back_populates="huesped", cascade="all, delete-orphan")
    favoritos = relationship("Favorito", back_populates="usuario", cascade="all, delete-orphan")
    resenas = relationship("Resena", back_populates="autor", cascade="all, delete-orphan")
    saldo_horas = relationship("SaldoHoras", uselist=False, cascade="all, delete-orphan")
    transacciones_horas = relationship("TransaccionHoras", cascade="all, delete-orphan")