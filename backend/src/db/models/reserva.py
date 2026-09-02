from sqlalchemy import Column, Integer, Date, Numeric, String, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from src.db.connection import Base
import enum


class EstadoReserva(str, enum.Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    RECHAZADA = "rechazada"
    CANCELADA = "cancelada"
    FINALIZADA = "finalizada"


class MetodoPago(str, enum.Enum):
    DINERO = "dinero"
    HORAS = "horas"


class Reserva(Base):
    __tablename__ = "reserva"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    propiedad_id = Column(Integer, ForeignKey("propiedad.id", ondelete="CASCADE"), nullable=False)
    huesped_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    estado = Column(String(20), nullable=False, default=EstadoReserva.PENDIENTE.value)
    total = Column(Numeric(10, 2), nullable=False)

    metodo_pago = Column(String(20), nullable=False, default=MetodoPago.DINERO.value)
    horas_utilizadas = Column(Integer, nullable=True)
    horas_ganadas = Column(Integer, nullable=True)

    propiedad = relationship("Propiedad", back_populates="reservas")
    huesped = relationship("Usuario", back_populates="reservas")
    resena = relationship("Resena", uselist=False, back_populates="reserva", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("fecha_fin > fecha_inicio", name="chk_fechas_reserva"),
        CheckConstraint("total >= 0", name="chk_total"),
        Index("idx_reserva_fechas", "fecha_inicio", "fecha_fin"),
    )