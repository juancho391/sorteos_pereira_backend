from .models import UserCreate
from ..db.conexion import session_dependency
from ..entities.User import Users
from sqlmodel import select


def crearUser(session: session_dependency, user_compra: UserCreate):
    nuevo_usuario = Users.model_validate(user_compra)
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    return nuevo_usuario


def obtenerUsuario(session: session_dependency, cedula: str):
    user = session.exec(select(Users).where(Users.cedula == cedula)).first()
    if not user:
        return False
    return user
