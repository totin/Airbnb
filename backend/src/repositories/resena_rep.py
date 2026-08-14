from sqlalchemy.orm import Session

from src.db.models.resena import Resena


class ResenaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, 
        reserva_id: int, 
        autor_id: int, 
        puntaje: int, 
        comentario: str | None = None
    ) -> Resena:
        
        resena = Resena(
            reserva_id=reserva_id,
            autor_id=autor_id,
            puntaje=puntaje,
            comentario=comentario
        )
        self.db.add(resena)
        self.db.commit()
        self.db.refresh(resena)
        return resena

    def get_by_id(self, resena_id: int) -> Resena | None:
        
        return self.db.query(Resena).filter(Resena.id == resena_id).first()

    def get_by_reserva_id(self, reserva_id: int) -> Resena | None:
        
        return self.db.query(Resena).filter(Resena.reserva_id == reserva_id).first()

    def update(self, resena: Resena) -> Resena:
       
        self.db.add(resena)
        self.db.commit()
        self.db.refresh(resena)
        return resena

    def delete(self, resena: Resena) -> None:
        
        self.db.delete(resena)
        self.db.commit()