from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar el manejador de errores de tu carpeta utils
from src.middlewares.error_middleware import app_error_handler
from src.utils.errors import AppError

# Importar los routers de TU proyecto
from src.routers import (
    usuario_router,
    propiedad_router,
    reserva_router,
    resena_router,
    amenidad_router,
    favorito_router,
)

app = FastAPI(title="Airbnb Clone API", version="1.0.0")

# Manejador de excepciones global
app.add_exception_handler(AppError, app_error_handler)

# Habilitar CORS para que el frontend pueda conectarse sin bloqueos
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar los routers de Airbnb
app.include_router(usuario_router.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(propiedad_router.router, prefix="/api/propiedades", tags=["Propiedades"])
app.include_router(reserva_router.router, prefix="/api/reservas", tags=["Reservas"])
app.include_router(resena_router.router, prefix="/api/resenas", tags=["Reseñas"])
app.include_router(amenidad_router.router, prefix="/api/amenidades", tags=["Amenidades"])
app.include_router(favorito_router.router, prefix="/api/favoritos", tags=["Favoritos"])


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}