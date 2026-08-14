from src.db.models.usuario_model import Usuario
from src.dtos.usuario_dto import CreateUsuarioDTO, UsuarioResponseDTO


def usuario_create_to_model(dto: CreateUsuarioDTO) -> Usuario:
    return Usuario(
        nombre=dto.nombre,
        email=dto.email,
        es_anfitrion=dto.es_anfitrion
    )


def usuario_to_response(usuario: Usuario) -> UsuarioResponseDTO:
    return UsuarioResponseDTO.model_validate(usuario)