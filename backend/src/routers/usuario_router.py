from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.db.models.usuario import Usuario
from src.dtos.usuario_dto import CreateUsuarioDTO, UsuarioResponseDTO
from src.middlewares.auth_middleware import get_current_user
from src.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post(
    "",
    response_model=UsuarioResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario"
)
def registrar_usuario(
    usuario_data: CreateUsuarioDTO,
    db: Session = Depends(get_db)
):
    """HU1: Permite a un nuevo usuario registrarse en la plataforma."""
    usuario_service = UsuarioService(db)
    return usuario_service.crear_usuario(usuario_data)


@router.get(
    "/me",
    response_model=UsuarioResponseDTO,
    summary="Obtener el perfil del usuario actual"
)
def obtener_mi_perfil(
    current_user: Usuario = Depends(get_current_user)
):
    """Devuelve la información del usuario autenticado leyendo su Token."""
    return current_user