from sqlalchemy import Column, Integer, Date, Numeric, Enum, ForeignKey, CheckConstraint, Index
from database import Base
import enum

class EstadoReserva(str, enum.Enum):
    PENDIENTE = 'pendiente'
    CONFIRMADA = 'confirmada'
    CANCELADA = 'cancelada'
    FINALIZADA = 'finalizada'

class Reserva(Base):
    __tablename__ = "reserva"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    propiedad_id = Column(Integer, ForeignKey("propiedad.id", ondelete="CASCADE"), nullable=False)
    huesped_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    estado = Column(
        Enum(EstadoReserva), 
        nullable=False, 
        default=EstadoReserva.PENDIENTE
    )
    total = Column(Numeric(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("fecha_fin > fecha_inicio", name="chk_fechas_reserva"),
        CheckConstraint("total >= 0", name="chk_total"),
        Index("idx_reserva_fechas", "fecha_inicio", "fecha_fin"),
    )