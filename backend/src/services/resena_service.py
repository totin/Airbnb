from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from src.db.models.resena import Resena
from src.db.models.reserva import Reserva
from src.db.models.usuario import Usuario
from src.dtos.usuario_dto import UsuarioResponseDTO


class ResenaService:

    def __init__(self, db: Session):
        self.db = db

    def _enriquecer_resena(self, resena: Resena) -> dict:
        autor_dto = None
        if resena.autor:
            autor_dto = UsuarioResponseDTO(
                id=resena.autor.id,
                email=resena.autor.email,
                nombre=resena.autor.nombre,
                fecha_registro=resena.autor.fecha_registro,
                es_anfitrion=resena.autor.es_anfitrion,
            )

        prop_id = resena.reserva.propiedad_id if resena.reserva else None

        return {
            "id": resena.id,
            "reserva_id": resena.reserva_id,
            "autor_id": resena.autor_id,
            "propiedad_id": prop_id,
            "puntaje": resena.puntaje,
            "comentario": resena.comentario,
            "fecha": resena.fecha,
            "autor": autor_dto,
        }

    def crear_resena(
        self,
        reserva_id: int,
        autor_id: int,
        puntaje: int,
        comentario: Optional[str] = None,
    ) -> dict:
        if not (1 <= puntaje <= 5):
            raise ValueError("El puntaje debe ser un número entero entre 1 y 5.")

        reserva = self.db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if not reserva:
            raise ValueError(f"No existe ninguna reserva con ID {reserva_id}.")

        if reserva.huesped_id != autor_id:
            raise ValueError("Solo el huésped que realizó la reserva puede dejar una reseña.")

        if reserva.estado not in ["confirmada", "finalizada"]:
            raise ValueError("Solo se pueden reseñar reservas confirmadas o finalizadas.")

        if reserva.fecha_fin > date.today():
            raise ValueError("La estadía todavía no terminó.")

        resena_existente = self.db.query(Resena).filter(Resena.reserva_id == reserva_id).first()
        if resena_existente:
            raise ValueError("Esta reserva ya posee una reseña registrada.")

        resena = Resena(
            reserva_id=reserva_id,
            autor_id=autor_id,
            puntaje=puntaje,
            comentario=comentario,
            fecha=date.today(),
        )
        self.db.add(resena)
        self.db.commit()
        self.db.refresh(resena)
        return self._enriquecer_resena(resena)

    def obtener_por_id(self, resena_id: int) -> dict:
        resena = self.db.query(Resena).filter(Resena.id == resena_id).first()
        if not resena:
            raise ValueError(f"No se encontró la reseña con ID {resena_id}.")
        return self._enriquecer_resena(resena)

    def listar_por_propiedad(self, propiedad_id: int) -> list[dict]:
        resenas = (
            self.db.query(Resena)
            .join(Reserva, Resena.reserva_id == Reserva.id)
            .filter(Reserva.propiedad_id == propiedad_id)
            .order_by(Resena.fecha.desc())
            .all()
        )
        return [self._enriquecer_resena(r) for r in resenas]