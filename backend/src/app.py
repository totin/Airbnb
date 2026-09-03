import os
import shutil
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Importaciones de la base de datos
from src.db.connection import Base, engine
import src.db.models
from src.db.init_db import init_database

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
    horas_router,
    lugares_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Asegurar inicialización y consistencia de tablas y columnas
    try:
        init_database()
    except Exception as e:
        print(f"Aviso durante init_database en startup: {e}")
    yield


# 2. Inicializar la aplicación FastAPI
app = FastAPI(
    title="API Airbnb Clone",
    description="Backend para plataforma de reservas y propiedades",
    version="1.0.0",
    lifespan=lifespan,
)

# 3. Crear la carpeta para imágenes y servirla como archivos estáticos
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 4. Configurar CORS para permitir comunicación con el Frontend
# 4. Configurar CORS para permitir comunicación con el Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 5. Registrar los endpoints
app.include_router(usuario_router)
app.include_router(anfitrion_router)
app.include_router(amenidad_router)
app.include_router(propiedad_router)
app.include_router(propiedad_amenidad_router)
app.include_router(reserva_router)
app.include_router(resena_router)
app.include_router(favorito_router)
app.include_router(horas_router)
app.include_router(lugares_router)


@app.get("/")
def root():
    return {"message": "API de Airbnb Clone funcionando correctamente"}


# 6. Endpoint para recibir y guardar imágenes
@app.post("/upload-imagen")
async def subir_imagen(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1] or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join("uploads", filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"url": f"/uploads/{filename}"}
