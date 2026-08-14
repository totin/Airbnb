from datetime import date
from sqlalchemy.orm import Session
from src.repositories.reserva_repository import ReservaRepository
from src.repositories.propiedad_repository import PropiedadRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.db.models.reserva import Reserva  # Tu modelo ORM SQLAlchemy


class ReservaService:

    def __init__(self, db: Session):
        self.reserva_repo = ReservaRepository(db)
        self.propiedad_repo = PropiedadRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    def crear_reserva(
        self,
        propiedad_id: int,
        huesped_id: int,
        fecha_inicio: date,
        fecha_fin: date
    ) -> Reserva:
        """Crea una reserva aplicando todas las validaciones de negocio."""
        
        # 1. Regla de negocio: Validar rango de fechas
        if fecha_fin <= fecha_inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio.")

        # 2. Regla de negocio: Verificar existencia de la propiedad
        propiedad = self.propiedad_repo.get_by_id(propiedad_id)
        if not propiedad:
            raise ValueError(f"No existe ninguna propiedad con ID {propiedad_id}.")

        # 3. Regla de negocio: Verificar existencia del huésped
        huesped = self.usuario_repo.get_by_id(huesped_id)
        if not huesped:
            raise ValueError(f"No existe ningún usuario con ID {huesped_id}.")

        # 4. Regla de negocio: El anfitrión no puede reservar su propia propiedad
        if propiedad.anfitrion_id == huesped_id:
            raise ValueError("El anfitrión no puede realizar una reserva en su propia propiedad.")

        # 5. Regla de negocio: Comprobar solapamiento de fechas con reservas activas
        hay_solapamiento = self.reserva_repo.existe_solapamiento(
            propiedad_id=propiedad_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        if hay_solapamiento:
            raise ValueError("La propiedad no se encuentra disponible para las fechas seleccionadas.")

        # 6. Cálculo de negocio: Calcular el total en base al precio por noche
        noches = (fecha_fin - fecha_inicio).days
        total_calculado = noches * propiedad.precio_noche

        # Guardar en base de datos mediante el repositorio
        return self.reserva_repo.create(
            propiedad_id=propiedad_id,
            huesped_id=huesped_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            total=total_calculado,
            estado="pendiente"
        )

    def obtener_por_id(self, reserva_id: int) -> Reserva:
        """Obtiene una reserva por ID o lanza error si no existe."""
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValueError(f"No se encontró la reserva con ID {reserva_id}.")
        return reserva

    def listar_por_huesped(self, huesped_id: int) -> list[Reserva]:
        """Obtiene el historial de reservas asociadas a un huésped."""
        return self.reserva_repo.get_by_huesped_id(huesped_id)

    def cancelar_reserva(self, reserva_id: int, usuario_id: int) -> Reserva:
        """Permite cancelar una reserva existente."""
        reserva = self.obtener_por_id(reserva_id)

        # Regla de negocio: Solo el huésped que reservó o el anfitrión pueden cancelar
        if reserva.huesped_id != usuario_id and reserva.propiedad.anfitrion_id != usuario_id:
            raise ValueError("No tienes permisos para cancelar esta reserva.")

        if reserva.estado == "cancelada":
            raise ValueError("La reserva ya se encuentra cancelada.")

        if reserva.estado == "finalizada":
            raise ValueError("No se puede cancelar una reserva que ya ha finalizado.")

        return self.reserva_repo.update(reserva, estado="cancelada")