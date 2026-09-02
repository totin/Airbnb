from sqlalchemy.orm import Session

from src.db.models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, email: str, nombre: str, es_anfitrion: bool = False) -> Usuario:
       
        usuario = Usuario(
            email=email,
            nombre=nombre,
            es_anfitrion=es_anfitrion
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def get_by_id(self, usuario_id: int) -> Usuario | None:
        
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def get_by_email(self, email: str) -> Usuario | None:
        
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def get_all(self) -> list[Usuario]:
        return self.db.query(Usuario).order_by(Usuario.id).all()

    def update(self, usuario: Usuario, **changes) -> Usuario:
        for field, value in changes.items():
            setattr(usuario, field, value)
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, usuario: Usuario) -> None:
        
        self.db.delete(usuario)
        self.db.commit()