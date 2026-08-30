from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
from src.db.connection import Base
import enum


class TipoTransaccionHoras(str, enum.Enum):
    GANADA = "ganada"
    GASTADA = "gastada"
    DEVUELTA = "devuelta"
    AJUSTE = "ajuste"


class TransaccionHoras(Base):
    __tablename__ = "transacciones_horas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    reserva_id = Column(Integer, ForeignKey("reserva.id", ondelete="SET NULL"), nullable=True)
    tipo = Column(Enum(TipoTransaccionHoras), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha = Column(DateTime, server_default=func.now())