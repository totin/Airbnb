from typing import Optional
from backend.src.db.models import propiedad
from sqlalchemy.orm import Session
from src.repositories.propiedad_repository import PropiedadRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.db.models.propiedad import Propiedad  # Tu modelo ORM SQLAlchemy


class PropiedadService:

    def __init__(self, db: Session):
        self.propiedad_repo = PropiedadRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    def crear_propiedad(
        self,
        titulo: str,
        direccion: str,
        ciudad: str,
        precio_noche: float,
        capacidad: int,
        anfitrion_id: int
    ) -> Propiedad:
        """Crea una nueva propiedad validando las reglas de negocio."""
        
        # 1. Regla de negocio: El usuario debe existir
        anfitrion = self.usuario_repo.get_by_id(anfitrion_id)
        if not anfitrion:
            raise ValueError(f"No existe ningún usuario con ID {anfitrion_id}.")

        # 2. Regla de negocio: El usuario debe ser anfitrión
        if not anfitrion.es_anfitrion:
            raise ValueError(
                f"El usuario con ID {anfitrion_id} no tiene permisos de anfitrión para publicar propiedades."
            )

        # 3. Reglas de negocio: Validar restricciones cuantitativas
        if precio_noche <= 0:
            raise ValueError("El precio por noche debe ser mayor a 0.")
            
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser de al menos 1 huésped.")

        # Guardar mediante el repositorio
        return self.propiedad_repo.create(
            titulo=titulo,
            direccion=direccion,
            ciudad=ciudad,
            precio_noche=precio_noche,
            capacidad=capacidad,
            anfitrion_id=anfitrion_id
        )

    def obtener_por_id(self, propiedad_id: int) -> Propiedad:
        """Obtiene una propiedad por su ID o lanza error si no existe."""
        propiedad = self.propiedad_repo.get_by_id(propiedad_id)
        if not propiedad:
            raise ValueError(f"No se encontró la propiedad con ID {propiedad_id}.")
        return propiedad

    def buscar_propiedades(
        self, 
        ciudad: Optional[str] = None, 
        capacidad_minima: Optional[int] = None
    ) -> list[Propiedad]:
        """Busca propiedades aplicando filtros opcionales (por ciudad o cantidad de huéspedes)."""
        return self.propiedad_repo.buscar(
            ciudad=ciudad, 
            capacidad_minima=capacidad_minima
        )

    def listar_por_anfitrion(self, anfitrion_id: int) -> list[Propiedad]:
        """Obtiene todas las propiedades creadas por un anfitrión específico."""
        anfitrion = self.usuario_repo.get_by_id(anfitrion_id)
        if not anfitrion:
            raise ValueError(f"No existe ningún usuario con ID {anfitrion_id}.")
            
        return self.propiedad_repo.get_by_anfitrion_id(anfitrion_id)

    def eliminar_propiedad(self, propiedad_id: int, anfitrion_id: int) -> None:
        propiedad = self.propiedad_repo.obtener_por_id(propiedad_id)

        if not propiedad:
            raise ValueError(f"No se encontró la propiedad con ID {propiedad_id}.")

        if propiedad.anfitrion_id != anfitrion_id:
            raise ValueError("No tienes permiso para eliminar esta propiedad.")

        self.propiedad_repo.eliminar(propiedad)