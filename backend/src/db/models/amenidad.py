from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.connection import Base


class Amenidad(Base):
    __tablename__ = "amenidad"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)

    propiedades = relationship(
        "Propiedad",
        secondary="propiedad_amenidades",
        back_populates="amenidades",
    )