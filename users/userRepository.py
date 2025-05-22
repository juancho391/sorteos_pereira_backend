from ..entities.User import Users
from fastapi import Depends
from typing import Annotated
from .models import UserCreate
from ..db.conexion import session_dependency
from sqlmodel import select


class UserRepository:
    def __init__(self, session: session_dependency):
        self.session = session

    def crear_usuario(self, usuario: UserCreate):
        nuevo_usuario = Users.model_validate(usuario)
        self.session.add(nuevo_usuario)
        self.session.commit()
        self.session.refresh(nuevo_usuario)
        return nuevo_usuario

    def obtener_usuarios(self):
        return self.session.exec(select(Users).where(Users.is_admin == False)).all()

    def obtener_usuario_cedula(self, cedula: str):
        return self.session.exec(select(Users).where(Users.cedula == cedula)).first()

    def obtener_usuario_id(self, id_user: int):
        return self.session.get(Users, id_user)


def get_user_repository(session: session_dependency):
    return UserRepository(session=session)


user_repository_dependency = Annotated[UserRepository, Depends(get_user_repository)]
