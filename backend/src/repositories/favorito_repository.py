from sqlalchemy.orm import Session
from src.db.models.favorito import Favorito


class FavoritoRepository:

    def __init__(self, db: Session):
        self.db = db

    def existe_favorito(self, usuario_id: int, propiedad_id: int) -> bool:
        return self.db.query(Favorito).filter(
            Favorito.usuario_id == usuario_id,
            Favorito.propiedad_id == propiedad_id
        ).first() is not None

    def get_favorito(self, usuario_id: int, propiedad_id: int) -> Favorito | None:
        return self.db.query(Favorito).filter(
            Favorito.usuario_id == usuario_id,
            Favorito.propiedad_id == propiedad_id
        ).first()

    def get_by_usuario_id(self, usuario_id: int) -> list[Favorito]:
        return self.db.query(Favorito).filter(Favorito.usuario_id == usuario_id).all()

    def create(self, usuario_id: int, propiedad_id: int) -> Favorito:
        favorito = Favorito(usuario_id=usuario_id, propiedad_id=propiedad_id)
        self.db.add(favorito)
        self.db.commit()
        self.db.refresh(favorito)
        return favorito

    def delete(self, favorito: Favorito):
        self.db.delete(favorito)
        self.db.commit()
        return favorito