from .models import UserCreate
from typing import Annotated
from fastapi import Depends
from .userRepository import user_repository_dependency


class UserService:
    def __init__(self, users_repository: user_repository_dependency):
        self.users_repository = users_repository

    def obtener_usuarios(self):
        usuarios = self.users_repository.obtener_usuarios()
        if not usuarios:
            return []
        return usuarios

    def crear_usuario(self, usuario: UserCreate):
        usuarios_existentes = self.obtener_usuarios()
        for user in usuarios_existentes:
            if user.cedula == usuario.cedula:
                return False
        return self.users_repository.crear_usuario(usuario=usuario)

    def obtener_usuario_cedula(self, cedula: str):
        usuario = self.users_repository.obtener_usuario_cedula(cedula=cedula)
        if not usuario:
            return False
        return usuario

    def obtener_usuario_id(self, id_user: int):
        usuario = self.users_repository.obtener_usuario_id(id_user=id_user)
        if not usuario:
            return False
        return usuario


def get_users_service(users_repository: user_repository_dependency):
    return UserService(users_repository=users_repository)


user_service_dependency = Annotated[UserService, Depends(get_users_service)]
