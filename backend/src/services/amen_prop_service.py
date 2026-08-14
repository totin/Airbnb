from sqlalchemy.orm import Session
from src.repositories.propiedad_amenidad_repository import PropiedadAmenidadRepository
from src.repositories.propiedad_repository import PropiedadRepository
from src.repositories.amenidad_repository import AmenidadRepository


class PropiedadAmenidadService:

    def __init__(self, db: Session):
        self.pa_repo = PropiedadAmenidadRepository(db)
        self.propiedad_repo = PropiedadRepository(db)
        self.amenidad_repo = AmenidadRepository(db)

    def asociar_amenidad(self, propiedad_id: int, amenidad_id: int):
        """Asocia una amenidad a una propiedad validando su existencia previa."""
        
        # 1. Regla de negocio: Verificar que la propiedad exista
        propiedad = self.propiedad_repo.get_by_id(propiedad_id)
        if not propiedad:
            raise ValueError(f"No existe ninguna propiedad con ID {propiedad_id}.")

        # 2. Regla de negocio: Verificar que la amenidad exista
        amenidad = self.amenidad_repo.get_by_id(amenidad_id)
        if not amenidad:
            raise ValueError(f"No existe ninguna amenidad con ID {amenidad_id}.")

        # 3. Regla de negocio: Comprobar si ya está vinculada
        ya_existe = self.pa_repo.existe_relacion(propiedad_id, amenidad_id)
        if ya_existe:
            raise ValueError("La propiedad ya cuenta con esta amenidad asociada.")

        return self.pa_repo.create(propiedad_id=propiedad_id, amenidad_id=amenidad_id)

    def asociar_multiples_amenidades(self, propiedad_id: int, amenidades_ids: list[int]):
        """Asocia una lista de IDs de amenidades a una propiedad."""
        # Verificar propiedad
        propiedad = self.propiedad_repo.get_by_id(propiedad_id)
        if not propiedad:
            raise ValueError(f"No existe ninguna propiedad con ID {propiedad_id}.")

        # Asociar cada amenidad no duplicada
        for amenidad_id in amenidades_ids:
            amenidad = self.amenidad_repo.get_by_id(amenidad_id)
            if amenidad and not self.pa_repo.existe_relacion(propiedad_id, amenidad_id):
                self.pa_repo.create(propiedad_id=propiedad_id, amenidad_id=amenidad_id)

    def desasociar_amenidad(self, propiedad_id: int, amenidad_id: int):
        """Remueve una amenidad específica de una propiedad."""
        relacion = self.pa_repo.get_relacion(propiedad_id, amenidad_id)
        if not relacion:
            raise ValueError("La amenidad especificada no está asociada a esta propiedad.")

        return self.pa_repo.delete(relacion)