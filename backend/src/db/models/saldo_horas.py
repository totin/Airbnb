from sqlalchemy import Column, Integer, ForeignKey
from src.db.connection import Base


class SaldoHoras(Base):
    __tablename__ = "saldo_horas"

    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), primary_key=True)
    horas = Column(Integer, default=0, nullable=False)