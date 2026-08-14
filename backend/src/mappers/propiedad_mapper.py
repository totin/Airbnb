from db.models.propiedad import Propiedad  # Ajusta la importación según la ruta de tu modelo
from dtos.propiedad_dto import CreatePropiedadDTO, UpdatePropiedadDTO, PropiedadResponseDTO


class PropiedadMapper:

    @staticmethod
    def dto_to_entity(dto: CreatePropiedadDTO) -> Propiedad:
        
        return Propiedad(
            titulo=dto.titulo,
            direccion=dto.direccion,
            ciudad=dto.ciudad,
            precio_noche=dto.precio_noche,
            capacidad=dto.capacidad,
            anfitrion_id=dto.anfitrion_id
        )

    @staticmethod
    def entity_to_dto(entity: Propiedad) -> PropiedadResponseDTO:
       
        return PropiedadResponseDTO(
            id=entity.id,
            titulo=entity.titulo,
            direccion=entity.direccion,
            ciudad=entity.ciudad,
            precio_noche=float(entity.precio_noche),
            capacidad=entity.capacidad,
            anfitrion_id=entity.anfitrion_id
        )

    @staticmethod
    def update_entity_from_dto(dto: UpdatePropiedadDTO, entity: Propiedad) -> Propiedad:
       
        if dto.titulo is not None:
            entity.titulo = dto.titulo
        if dto.direccion is not None:
            entity.direccion = dto.direccion
        if dto.ciudad is not None:
            entity.ciudad = dto.ciudad
        if dto.precio_noche is not None:
            entity.precio_noche = dto.precio_noche
        if dto.capacidad is not None:
            entity.capacidad = dto.capacidad

        return entity