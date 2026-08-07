from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    fecha_registro = Column(DateTime, server_default=func.now())
    es_anfitrion = Column(Boolean, default=False, nullable=False)