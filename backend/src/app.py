from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importaciones de la base de datos
from src.db.connection import Base, engine
import src.db.models  # Necesario para que SQLAlchemy registre todas las tablas

# Importaciones de los routers
from src.routers import (
    usuario_router,
    anfitrion_router,
    amenidad_router,
    propiedad_router,
    propiedad_amenidad_router,
    reserva_router,
    resena_router,
    favorito_router,
)

# 1. Crear las tablas en PostgreSQL (pgAdmin) si aún no existen
Base.metadata.create_all(bind=engine)

# 2. Inicializar la aplicación FastAPI
app = FastAPI(
    title="API Airbnb Clone",
    description="Backend para plataforma de reservas y propiedades",
    version="1.0.0"
)

# 3. Configurar CORS para permitir comunicación con el Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Registrar los endpoints
app.include_router(usuario_router)
app.include_router(anfitrion_router)
app.include_router(amenidad_router)
app.include_router(propiedad_router)
app.include_router(propiedad_amenidad_router)
app.include_router(reserva_router)
app.include_router(resena_router)
app.include_router(favorito_router)


@app.get("/")
def root():
    return {"message": "API de Airbnb Clone funcionando correctamente"}