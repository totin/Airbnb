from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.db.connection import get_db
from src.dtos.lugares_dto import LugarTuristicoDTO, LugarConCercanasDTO
from src.services.lugares_service import LugaresService

router = APIRouter(prefix="/lugares", tags=["Lugares Turísticos"])


@router.get("", response_model=list[LugarTuristicoDTO])
def listar_lugares(ciudad: Optional[str] = None):
    service = LugaresService()
    return service.listar_lugares(ciudad=ciudad)


@router.get("/cercanias", response_model=list[LugarConCercanasDTO])
def lugares_con_cercanias(
    ciudad: Optional[str] = None,
    radio_km: float = Query(25.0, description="Radio en kilómetros"),
    db: Session = Depends(get_db),
):
    service = LugaresService()
    return service.get_lugares_con_cercanias(db, ciudad=ciudad, radio_km=radio_km)
