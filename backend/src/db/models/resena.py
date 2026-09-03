from sqlalchemy import Column, Integer, ForeignKey, Date, Text, CheckConstraint, func
from sqlalchemy.orm import relationship
from src.db.connection import Base


class Resena(Base):
    __tablename__ = "resena"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reserva_id = Column(
        Integer,
        ForeignKey("reserva.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    autor_id = Column(
        Integer,
        ForeignKey("usuario.id", ondelete="CASCADE"),
        nullable=False,
    )
    puntaje = Column(Integer, nullable=False)
    comentario = Column(Text, nullable=True)
    fecha = Column(
        Date,
        nullable=False,
        server_default=func.current_date(),
    )

    reserva = relationship("Reserva", back_populates="resena")
    autor = relationship("Usuario", back_populates="resenas")

    __table_args__ = (
        CheckConstraint(
            "puntaje BETWEEN 1 AND 5",
            name="chk_puntaje",
        ),
    )