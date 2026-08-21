from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.connection import get_db
from src.dtos.usuario_dto import UsuarioResponseDTO
from src.dtos.propiedad_dto import PropiedadResponseDTO
from src.services.usuario_service import UsuarioService
from src.services.propiedad_service import PropiedadService

router = APIRouter(prefix="/anfitriones", tags=["Anfitriones"])


@router.patch("/{usuario_id}/activar", response_model=UsuarioResponseDTO)
def convertir_en_anfitrion(usuario_id: int, db: Session = Depends(get_db)):
    """Otorga permisos de anfitrión a un usuario existente."""
    usuario_service = UsuarioService(db)
    try:
        return usuario_service.convertir_en_anfitrion(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{anfitrion_id}/propiedades", response_model=list[PropiedadResponseDTO])
def listar_propiedades_de_anfitrion(anfitrion_id: int, db: Session = Depends(get_db)):
    """Obtiene el listado de propiedades asociadas a un anfitrión."""
    propiedad_service = PropiedadService(db)
    try:
        return propiedad_service.listar_por_anfitrion(anfitrion_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{anfitrion_id}", response_model=UsuarioResponseDTO)
def obtener_perfil_anfitrion(anfitrion_id: int, db: Session = Depends(get_db)):
    """Obtiene la información de un usuario validando que sea anfitrión."""
    usuario_service = UsuarioService(db)
    try:
        usuario = usuario_service.obtener_por_id(anfitrion_id)
        if not usuario.es_anfitrion:
            raise HTTPException(
                status_code=400,
                detail=f"El usuario con ID {anfitrion_id} no es anfitrión."
            )
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))