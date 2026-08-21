from sqlalchemy import Column, Integer, ForeignKey, Date, Text, CheckConstraint, func
from src.db.connection import Base

class Resena(Base):
    __tablename__ = "resenas"
    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(
        Integer,
        ForeignKey("reserva.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    autor_id = Column(
        Integer,
        ForeignKey("usuario.id", ondelete="CASCADE"),
        nullable=False
    )
    puntaje = Column(
        Integer,
        nullable=False
    )
    comentario = Column(Text)
    fecha = Column(
        Date,
        nullable=False,
        server_default=func.current_date()
    )
    __table_args__ = (
        CheckConstraint(
            "puntaje BETWEEN 1 AND 5",
            name="chk_puntaje"
        ),
    )