from sqlalchemy.orm import Session
from src.db.models.favorito import Favorito
from src.db.models.propiedad import Propiedad


class FavoritoRepository:

    def __init__(self, db: Session):
        self.db = db

    def crear(self, favorito: Favorito) -> Favorito:
        self.db.add(favorito)
        self.db.commit()
        self.db.refresh(favorito)
        return favorito

    def obtener(
        self,
        usuario_id: int,
        propiedad_id: int
    ) -> Favorito | None:

        return (
            self.db.query(Favorito)
            .filter(
                Favorito.usuario_id == usuario_id,
                Favorito.propiedad_id == propiedad_id
            )
            .first()
        )

    def obtener_por_usuario(
        self,
        usuario_id: int
    ) -> list[Propiedad]:

        return (
            self.db.query(Propiedad)
            .join(
                Favorito,
                Favorito.propiedad_id == Propiedad.id
            )
            .filter(
                Favorito.usuario_id == usuario_id
            )
            .all()
        )

    def eliminar(
        self,
        favorito: Favorito
    ) -> None:

        self.db.delete(favorito)
        self.db.commit()