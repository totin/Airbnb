from db.models.amenidad import Amenidad  # Ajusta la ruta a tu modelo de DB
from dtos.amenidad_dto import CreateAmenidadDTO, AmenidadResponseDTO


class AmenidadMapper:

    @staticmethod
    def dto_to_entity(dto: CreateAmenidadDTO) -> Amenidad:
        """
        Convierte el DTO recibidode entrada a un objeto de SQLAlchemy Amenidad.
        """
        return Amenidad(
            nombre=dto.nombre
        )

    @staticmethod
    def entity_to_dto(entity: Amenidad) -> AmenidadResponseDTO:
        """
        Convierte el objeto Amenidad de la DB a un DTO de respuesta.
        """
        return AmenidadResponseDTO(
            id=entity.id,
            nombre=entity.nombre
        )

    @staticmethod
    def entity_list_to_dto_list(entities: list[Amenidad]) -> list[AmenidadResponseDTO]:
        """
        Útil cuando quieres devolver la lista completa de amenidades (HU8).
        """
        return [AmenidadMapper.entity_to_dto(entity) for entity in entities]