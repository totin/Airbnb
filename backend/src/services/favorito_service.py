from sqlalchemy.orm import Session
from src.repositories.favorito_repository import FavoritoRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.repositories.propiedad_repository import PropiedadRepository


class FavoritoService:

    def __init__(self, db: Session):
        self.favorito_repo = FavoritoRepository(db)
        self.usuario_repo = UsuarioRepository(db)
        self.propiedad_repo = PropiedadRepository(db)

    def agregar_favorito(self, usuario_id: int, propiedad_id: int):
        """Agrega una propiedad a la lista de favoritos de un usuario."""

        # 1. Regla de negocio: Validar que el usuario exista
        usuario = self.usuario_repo.get_by_id(usuario_id)
        if not usuario:
            raise ValueError(f"No existe ningún usuario con ID {usuario_id}.")

        # 2. Regla de negocio: Validar que la propiedad exista
        propiedad = self.propiedad_repo.get_by_id(propiedad_id)
        if not propiedad:
            raise ValueError(f"No existe ninguna propiedad con ID {propiedad_id}.")

        # 3. Regla de negocio: Verificar si ya está guardada en favoritos
        ya_es_favorito = self.favorito_repo.existe_favorito(usuario_id, propiedad_id)
        if ya_es_favorito:
            raise ValueError("Esta propiedad ya se encuentra guardada en tus favoritos.")

        # Guardar en base de datos mediante el repositorio
        return self.favorito_repo.create(usuario_id=usuario_id, propiedad_id=propiedad_id)

    def eliminar_favorito(self, usuario_id: int, propiedad_id: int):
        """Remueve una propiedad de la lista de favoritos del usuario."""
        favorito = self.favorito_repo.get_favorito(usuario_id, propiedad_id)
        if not favorito:
            raise ValueError("La propiedad especificada no está guardada en tus favoritos.")

        return self.favorito_repo.delete(favorito)

    def listar_favoritos_por_usuario(self, usuario_id: int):
        """Obtiene la lista completa de propiedades marcadas como favoritas por un usuario."""
        usuario = self.usuario_repo.get_by_id(usuario_id)
        if not usuario:
            raise ValueError(f"No existe ningún usuario con ID {usuario_id}.")

        return self.favorito_repo.get_by_usuario_id(usuario_id)