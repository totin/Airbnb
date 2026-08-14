from src.db.models.user_model import User
from src.dtos.user_dto import UserResponseDTO


def to_user_response(user: User) -> UserResponseDTO:
    return UserResponseDTO.model_validate(user)
