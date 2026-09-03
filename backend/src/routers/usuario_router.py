from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from src.db.connection import get_db
from src.dtos.usuario_dto import UsuarioCreateDTO, UsuarioResponseDTO
from src.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


class LoginDTO(BaseModel):
    email: EmailStr


@router.post("", response_model=UsuarioResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_usuario(dto: UsuarioCreateDTO, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    try:
        return service.crear_usuario(
            email=dto.email,
            nombre=dto.nombre,
            es_anfitrion=dto.es_anfitrion,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=UsuarioResponseDTO)
def login_usuario(dto: LoginDTO, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    try:
        return service.obtener_por_email(dto.email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=list[UsuarioResponseDTO])
def listar_usuarios(db: Session = Depends(get_db)):
    service = UsuarioService(db)
    return service.listar_usuarios()


@router.get("/email/{email}", response_model=UsuarioResponseDTO)
def obtener_usuario_por_email(email: str, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    try:
        return service.obtener_por_email(email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{usuario_id}", response_model=UsuarioResponseDTO)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    try:
        return service.obtener_por_id(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{usuario_id}/anfitrion", response_model=UsuarioResponseDTO)
def convertir_en_anfitrion(usuario_id: int, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    try:
        return service.convertir_en_anfitrion(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))