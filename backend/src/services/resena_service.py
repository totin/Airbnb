from typing import Optional
from sqlalchemy.orm import Session
from src.repositories.resena_repository import ResenaRepository
from src.repositories.reserva_repository import ReservaRepository
from src.db.models.resena import Resena  # Tu modelo ORM SQLAlchemy


class ResenaService:

    def __init__(self, db: Session):
        self.resena_repo = ResenaRepository(db)
        self.reserva_repo = ReservaRepository(db)

    def crear_resena(
        self,
        reserva_id: int,
        autor_id: int,
        puntaje: int,
        comentario: Optional[str] = None
    ) -> Resena:
        """Crea una reseña aplicando todas las validaciones de negocio."""

        # 1. Regla de negocio: Validar que el puntaje esté entre 1 y 5 (chk_puntaje)
        if not (1 <= puntaje <= 5):
            raise ValueError("El puntaje debe ser un número entero entre 1 y 5.")

        # 2. Regla de negocio: Verificar que la reserva exista
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValueError(f"No existe ninguna reserva con ID {reserva_id}.")

        # 3. Regla de negocio: Solo el huésped de la reserva puede dejar la reseña
        if reserva.huesped_id != autor_id:
            raise ValueError("Solo el huésped que realizó la reserva tiene permiso para calificarla.")

        # 4. Regla de negocio: La reserva debe estar finalizada para poder calificarla
        if reserva.estado != "finalizada":
            raise ValueError("Solo puedes dejar una reseña en reservas con estado 'finalizada'.")

        # 5. Regla de negocio (reserva_id UNIQUE): Comprobar que no exista una reseña previa
        resena_existente = self.resena_repo.get_by_reserva_id(reserva_id)
        if resena_existente:
            raise ValueError("Esta reserva ya posee una reseña registrada.")

        # Guardar en base de datos mediante el repositorio
        return self.resena_repo.create(
            reserva_id=reserva_id,
            autor_id=autor_id,
            puntaje=puntaje,
            comentario=comentario
        )

    def obtener_por_id(self, resena_id: int) -> Resena:
        """Obtiene una reseña por su ID o lanza un error si no existe."""
        resena = self.resena_repo.get_by_id(resena_id)
        if not resena:
            raise ValueError(f"No se encontró la reseña con ID {resena_id}.")
        return resena

    def listar_por_propiedad(self, propiedad_id: int) -> list[Resena]:
        """Obtiene todas las reseñas asociadas a las reservas de una propiedad."""
        return self.resena_repo.get_by_propiedad_id(propiedad_id)