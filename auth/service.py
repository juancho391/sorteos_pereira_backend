from ..db.conexion import session_dependency
from . import models
from ..exceptions import UserNotFoundError, AuthenticationError
from ..entities import User
from passlib.context import CryptContext
from sqlmodel import select
from datetime import datetime, timedelta, timezone
import jwt
from jwt import PyJWTError
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token")


# Funcion para verificar la contraseña
def verificar_contrasena(contrasena: str, contrasena_hash: str):
    return pwd_context.verify(contrasena, contrasena_hash)


# Funcion para hashear la contraseña
def obtener_contrasena_hash(contrasena: str):
    return pwd_context.hash(contrasena)


def autenticar_usuario(usuario: models.USerLogin, session: session_dependency):
    usuario_bd = session.exec(
        select(User.Users).where(User.Users.email == usuario.email)
    ).first()
    if not usuario_bd or not verificar_contrasena(
        contrasena=usuario.password, contrasena_hash=usuario_bd.password
    ):
        return False
    return usuario_bd


def crear_acces_token(email: str, usuario_id: int, expires_delta: timedelta):
    encode = {
        "sub": email,
        "id": usuario_id,
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario: str = payload.get("id")
        return models.TokenData(user_id=id_usuario)
    except PyJWTError:
        raise AuthenticationError()


def obtener_usuario_actual(token: Annotated[str, Depends(oauth2_bearer)]):
    return verificar_token(token=token)


Usuario_actual = Annotated[models.TokenData, Depends(obtener_usuario_actual)]


def login_usuario(usuario: models.USerLogin, session: session_dependency):
    usuario = autenticar_usuario(usuario=usuario, session=session)
    if not usuario:
        raise AuthenticationError()
    token = crear_acces_token(
        email=usuario.email,
        usuario_id=usuario.id,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return models.Token(access_token=token, token_type="bearer")


# def registrar_usuario(usuario: User.Users, session: session_dependency):
#     try:
#         usuario.password = obtener_contrasena_hash(contrasena=usuario.password)
#         session.add(usuario)
#         session.commit()
#         session.refresh(usuario)
#     except Exception as e:
#         raise UserNotFoundError(error=str(e))
#     return usuario
