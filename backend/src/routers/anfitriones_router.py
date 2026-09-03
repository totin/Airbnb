from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from src.db.connection import get_db
from src.db.models.propiedad import Propiedad
from src.db.models.reserva import Reserva
from src.dtos.usuario_dto import UsuarioResponseDTO
from src.dtos.propiedad_dto import PropiedadResponseDTO
from src.dtos.reserva_dto import ReservaResponseDTO
from src.dtos.ingresos_dto import IngresosAnfitrionDTO, IngresoDetalleDTO
from src.services.usuario_service import UsuarioService
from src.services.propiedad_service import PropiedadService
from src.services.reserva_service import ReservaService

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


@router.get("/{anfitrion_id}/reservas", response_model=list[ReservaResponseDTO])
def listar_reservas_de_anfitrion(anfitrion_id: int, db: Session = Depends(get_db)):
    """Obtiene el listado de reservas recibidas por un anfitrión."""
    reserva_service = ReservaService(db)
    return reserva_service.listar_por_anfitrion(anfitrion_id)


@router.get("/{anfitrion_id}/ingresos", response_model=IngresosAnfitrionDTO)
def obtener_ingresos_anfitrion(
    anfitrion_id: int,
    desde: date = Query(date(2020, 1, 1), description="Fecha inicio YYYY-MM-DD"),
    hasta: date = Query(date(2030, 12, 31), description="Fecha fin YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    """Calcula los ingresos facturados por un anfitrión en un período de tiempo."""
    if desde >= hasta:
        raise HTTPException(status_code=400, detail="La fecha desde debe ser anterior a hasta")

    props = db.query(Propiedad).filter(Propiedad.anfitrion_id == anfitrion_id).all()
    detalles = []
    gran_total = 0.0

    for p in props:
        reservas_conf = (
            db.query(Reserva)
            .filter(
                Reserva.propiedad_id == p.id,
                Reserva.estado == "confirmada",
                Reserva.fecha_inicio < hasta,
                Reserva.fecha_fin > desde,
            )
            .all()
        )
        total_prop = sum(float(r.total) for r in reservas_conf)
        gran_total += total_prop
        detalles.append(
            IngresoDetalleDTO(
                propiedad_id=p.id,
                titulo=p.titulo,
                total=total_prop,
                reservas=len(reservas_conf),
            )
        )

    return IngresosAnfitrionDTO(total=round(gran_total, 2), detalle=detalles)


@router.get("/{anfitrion_id}", response_model=UsuarioResponseDTO)
def obtener_perfil_anfitrion(anfitrion_id: int, db: Session = Depends(get_db)):
    """Obtiene la información de un usuario validando que sea anfitrión."""
    usuario_service = UsuarioService(db)
    try:
        usuario = usuario_service.obtener_por_id(anfitrion_id)
        if not usuario.es_anfitrion:
            raise HTTPException(
                status_code=400,
                detail=f"El usuario con ID {anfitrion_id} no es anfitrión.",
            )
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
