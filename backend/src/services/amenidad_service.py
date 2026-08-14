from sqlalchemy.orm import Session
from src.repositories.amenidad_repository import AmenidadRepository
from src.db.models.amenidad import Amenidad  # Tu modelo ORM SQLAlchemy


class AmenidadService:

    def __init__(self, db: Session):
        self.amenidad_repo = AmenidadRepository(db)

    def crear_amenidad(self, nombre: str) -> Amenidad:
        """Crea una nueva amenidad validando que no exista previamente."""
        # Limpiamos espacios innecesarios
        nombre_limpio = nombre.strip()

        if not nombre_limpio:
            raise ValueError("El nombre de la amenidad no puede estar vacío.")

        # Regla de negocio: El nombre debe ser único
        amenidad_existente = self.amenidad_repo.get_by_nombre(nombre_limpio)
        if amenidad_existente:
            raise ValueError(f"La amenidad '{nombre_limpio}' ya existe en el sistema.")

        # Guardar en base de datos mediante el repositorio
        return self.amenidad_repo.create(nombre=nombre_limpio)

    def obtener_por_id(self, amenidad_id: int) -> Amenidad:
        """Obtiene una amenidad por su ID o lanza error si no existe."""
        amenidad = self.amenidad_repo.get_by_id(amenidad_id)
        if not amenidad:
            raise ValueError(f"No se encontró la amenidad con ID {amenidad_id}.")
        return amenidad

    def listar_todas(self) -> list[Amenidad]:
        """Obtiene el catálogo completo de amenidades para mostrar en los filtros de búsqueda."""
        return self.amenidad_repo.get_all()