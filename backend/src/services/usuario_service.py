from sqlalchemy.orm import Session
from src.repositories.usuario_repository import UsuarioRepository
from src.db.models.usuario import Usuario  # Tu modelo ORM SQLAlchemy


class UsuarioService:

    def __init__(self, db: Session):
        self.usuario_repo = UsuarioRepository(db)

    def crear_usuario(self, email: str, nombre: str, es_anfitrion: bool = False) -> Usuario:
        """Crea un nuevo usuario asegurando que el email sea único."""
        # Regla de negocio: No se pueden registrar dos usuarios con el mismo email
        usuario_existente = self.usuario_repo.get_by_email(email)
        if usuario_existente:
            raise ValueError(f"El email '{email}' ya se encuentra registrado.")

        # Guardar en base de datos mediante el repositorio
        return self.usuario_repo.create(
            email=email,
            nombre=nombre,
            es_anfitrion=es_anfitrion
        )

    def obtener_por_id(self, usuario_id: int) -> Usuario:
        """Obtiene un usuario por su ID o lanza error si no existe."""
        usuario = self.usuario_repo.get_by_id(usuario_id)
        if not usuario:
            raise ValueError(f"No se encontró el usuario con ID {usuario_id}.")
        return usuario

    def obtener_por_email(self, email: str) -> Usuario:
        """Obtiene un usuario por su Email o lanza error si no existe."""
        usuario = self.usuario_repo.get_by_email(email)
        if not usuario:
            raise ValueError(f"No existe ningún usuario con el email '{email}'.")
        return usuario

    def listar_usuarios(self) -> list[Usuario]:
        """Obtiene la lista completa de usuarios."""
        return self.usuario_repo.get_all()

    def convertir_en_anfitrion(self, usuario_id: int) -> Usuario:
        """Cambia el rol de un usuario a anfitrión."""
        usuario = self.obtener_por_id(usuario_id)
        
        if usuario.es_anfitrion:
            raise ValueError("El usuario ya es anfitrión.")

        return self.usuario_repo.update(usuario, es_anfitrion=True)