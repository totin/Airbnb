from sqlalchemy import Column, Integer, String
from src.db.connection import Base

class Amenidad(Base):
    __tablename__ = "amenidades"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(100), unique=True, nullable=False)