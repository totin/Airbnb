from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from src.db.connection import get_db
from src.db.models.propiedad import Propiedad
from src.dtos.propiedad_dto import (
    PropiedadCreateDTO,
    PropiedadUpdateDTO,
    PropiedadResponseDTO,
    AsociarAmenidadesDTO,
    AgregarImagenesDTO,
)
from src.dtos.lugares_dto import LugarCercanoDTO
from src.services.prop_amen_service import PropiedadAmenidadService
from src.services.propiedad_service import PropiedadService
from src.services.lugares_service import LugaresService

router = APIRouter(prefix="/propiedades", tags=["Propiedades"])


@router.post("", response_model=PropiedadResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_propiedad(dto: PropiedadCreateDTO, db: Session = Depends(get_db)):
    service = PropiedadService(db)
    try:
        return service.crear_propiedad(
            titulo=dto.titulo,
            direccion=dto.direccion,
            ciudad=dto.ciudad,
            precio_noche=dto.precio_noche,
            capacidad=dto.capacidad,
            anfitrion_id=dto.anfitrion_id,
            amenidades=dto.amenidades,
            imagenes=dto.imagenes,
            lat=dto.lat,
            lng=dto.lng,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/top", response_model=list[PropiedadResponseDTO])
def top_propiedades(ciudad: Optional[str] = None, db: Session = Depends(get_db)):
    service = PropiedadService(db)
    return service.get_top_propiedades(ciudad=ciudad)


@router.get("", response_model=list[PropiedadResponseDTO])
def buscar_propiedades(
    ciudad: Optional[str] = None,
    desde: Optional[str] = None,
    hasta: Optional[str] = None,
    huespedes: Optional[int] = None,
    capacidad_minima: Optional[int] = None,
    precio_max: Optional[float] = None,
    amenidades: Optional[str] = None,
    db: Session = Depends(get_db),
):
    service = PropiedadService(db)
    cant_huespedes = huespedes or capacidad_minima
    amenidades_list = [a.strip() for a in amenidades.split(",") if a.strip()] if amenidades else None
    return service.buscar_propiedades(
        ciudad=ciudad,
        desde=desde,
        hasta=hasta,
        huespedes=cant_huespedes,
        precio_max=precio_max,
        amenidades=amenidades_list,
    )


@router.get("/{propiedad_id}", response_model=PropiedadResponseDTO)
def obtener_propiedad(propiedad_id: int, db: Session = Depends(get_db)):
    service = PropiedadService(db)
    try:
        return service.obtener_por_id(propiedad_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{propiedad_id}/disponibilidad")
def obtener_disponibilidad(
    propiedad_id: int,
    mes: Optional[str] = Query(None, description="Mes en formato YYYY-MM"),
    db: Session = Depends(get_db),
):
    service = PropiedadService(db)
    if not mes:
        mes = datetime.now().strftime("%Y-%m")
    try:
        return service.get_disponibilidad(propiedad_id, mes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{propiedad_id}/lugares", response_model=list[LugarCercanoDTO])
def obtener_lugares_cercanos(
    propiedad_id: int,
    radio_km: float = 40.0,
    db: Session = Depends(get_db),
):
    prop_service = PropiedadService(db)
    try:
        prop = prop_service.obtener_por_id(propiedad_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    lugares_service = LugaresService()
    return lugares_service.get_lugares_cercanos_a_propiedad(prop.get("lat"), prop.get("lng"), radio_km=radio_km)


@router.get("/anfitrion/{anfitrion_id}", response_model=list[PropiedadResponseDTO])
def listar_por_anfitrion(anfitrion_id: int, db: Session = Depends(get_db)):
    service = PropiedadService(db)
    try:
        return service.listar_por_anfitrion(anfitrion_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{propiedad_id}", response_model=PropiedadResponseDTO)
@router.put("/{propiedad_id}", response_model=PropiedadResponseDTO)
def editar_propiedad(
    propiedad_id: int,
    dto: PropiedadUpdateDTO,
    anfitrion_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    service = PropiedadService(db)
    # Si anfitrion_id no viene en query, podemos obtenerlo de la propiedad si no se valida usuario de sesión
    if anfitrion_id is None:
        prop = service.db.query(service.db.models.Propiedad if hasattr(service.db, 'models') else Propiedad).filter(Propiedad.id == propiedad_id).first()
        if not prop:
            raise HTTPException(status_code=404, detail=f"No existe la propiedad con ID {propiedad_id}")
        anfitrion_id = prop.anfitrion_id

    try:
        return service.actualizar_propiedad(
            propiedad_id=propiedad_id,
            anfitrion_id=anfitrion_id,
            datos=dto,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{propiedad_id}/amenidades", status_code=status.HTTP_200_OK)
def asociar_amenidades(
    propiedad_id: int,
    dto: AsociarAmenidadesDTO,
    db: Session = Depends(get_db),
):
    service = PropiedadAmenidadService(db)
    try:
        service.asociar_multiples_amenidades(propiedad_id, dto.amenidades_ids)
        return {"message": "Amenidades asociadas correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{propiedad_id}/amenidades/{amenidad_id}", status_code=status.HTTP_200_OK)
def desasociar_amenidad(propiedad_id: int, amenidad_id: int, db: Session = Depends(get_db)):
    service = PropiedadAmenidadService(db)
    try:
        service.desasociar_amenidad(propiedad_id, amenidad_id)
        return {"message": "Amenidad desasociada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{propiedad_id}/imagenes", response_model=PropiedadResponseDTO)
def agregar_imagenes(
    propiedad_id: int,
    dto: AgregarImagenesDTO,
    anfitrion_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    service = PropiedadService(db)
    if anfitrion_id is None:
        prop = service.db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
        if not prop:
            raise HTTPException(status_code=404, detail=f"No existe la propiedad con ID {propiedad_id}")
        anfitrion_id = prop.anfitrion_id

    try:
        return service.agregar_imagenes(propiedad_id, anfitrion_id, dto.imagenes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{propiedad_id}/imagenes/{imagen_id}", status_code=status.HTTP_200_OK)
def eliminar_imagen(
    propiedad_id: int,
    imagen_id: int,
    anfitrion_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    service = PropiedadService(db)
    if anfitrion_id is None:
        prop = service.db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
        if not prop:
            raise HTTPException(status_code=404, detail=f"No existe la propiedad con ID {propiedad_id}")
        anfitrion_id = prop.anfitrion_id

    try:
        service.eliminar_imagen(propiedad_id, imagen_id, anfitrion_id)
        return {"message": "Imagen eliminada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{propiedad_id}")
def eliminar_propiedad(
    propiedad_id: int,
    anfitrion_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    service = PropiedadService(db)
    if anfitrion_id is None:
        prop = service.db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
        if not prop:
            raise HTTPException(status_code=404, detail=f"No existe la propiedad con ID {propiedad_id}")
        anfitrion_id = prop.anfitrion_id

    try:
        service.eliminar_propiedad(
            propiedad_id=propiedad_id,
            anfitrion_id=anfitrion_id,
        )
        return {"message": "Propiedad eliminada correctamente"}
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
