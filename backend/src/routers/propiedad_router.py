from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.connection import get_db
from src.dtos.propiedad_dto import (
    PropiedadCreateDTO,
    PropiedadUpdateDTO,
    PropiedadResponseDTO,
    AsociarAmenidadesDTO,
    AgregarImagenesDTO,
)
from src.services.prop_amen_service import PropiedadAmenidadService
from src.services.propiedad_service import PropiedadService

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
            imagenes=dto.imagenes
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[PropiedadResponseDTO])
def buscar_propiedades(
    ciudad: Optional[str] = None,
    capacidad_minima: Optional[int] = None,
    db: Session = Depends(get_db)
):
    service = PropiedadService(db)
    return service.buscar_propiedades(ciudad=ciudad, capacidad_minima=capacidad_minima)


@router.get("/{propiedad_id}", response_model=PropiedadResponseDTO)
def obtener_propiedad(propiedad_id: int, db: Session = Depends(get_db)):
    service = PropiedadService(db)
    try:
        return service.obtener_por_id(propiedad_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/anfitrion/{anfitrion_id}", response_model=list[PropiedadResponseDTO])
def listar_por_anfitrion(anfitrion_id: int, db: Session = Depends(get_db)):
    service = PropiedadService(db)
    try:
        return service.listar_por_anfitrion(anfitrion_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{propiedad_id}", response_model=PropiedadResponseDTO)
def editar_propiedad(
    propiedad_id: int,
    anfitrion_id: int,
    dto: PropiedadUpdateDTO,
    db: Session = Depends(get_db)
):
    service = PropiedadService(db)
    try:
        return service.actualizar_propiedad(
            propiedad_id=propiedad_id,
            anfitrion_id=anfitrion_id,
            datos=dto
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{propiedad_id}/amenidades", status_code=status.HTTP_200_OK)
def asociar_amenidades(
    propiedad_id: int,
    dto: AsociarAmenidadesDTO,
    db: Session = Depends(get_db)
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
    anfitrion_id: int,
    dto: AgregarImagenesDTO,
    db: Session = Depends(get_db)
):
    service = PropiedadService(db)
    try:
        return service.agregar_imagenes(propiedad_id, anfitrion_id, dto.imagenes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{propiedad_id}/imagenes/{imagen_id}", status_code=status.HTTP_200_OK)
def eliminar_imagen(
    propiedad_id: int,
    imagen_id: int,
    anfitrion_id: int,
    db: Session = Depends(get_db)
):
    service = PropiedadService(db)
    try:
        service.eliminar_imagen(propiedad_id, imagen_id, anfitrion_id)
        return {"message": "Imagen eliminada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{propiedad_id}")
def eliminar_propiedad(
    propiedad_id: int,
    anfitrion_id: int,
    db: Session = Depends(get_db)
):
    service = PropiedadService(db)

    try:
        service.eliminar_propiedad(
            propiedad_id=propiedad_id,
            anfitrion_id=anfitrion_id
        )

        return {"message": "Propiedad eliminada correctamente"}

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )