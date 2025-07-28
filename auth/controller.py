from fastapi import APIRouter
from fastapi import status

from ..db.conexion import session_dependency
from ..entities.User import UserAdminCreate, UserResponse
from . import models, service

auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/token", status_code=status.HTTP_200_OK)
async def login(user: models.USerLogin, session: session_dependency):
    return service.login_usuario(usuario=user, session=session)


@auth_router.post("/register", response_model=UserResponse)
async def register(user: UserAdminCreate, session: session_dependency):
    return service.registrar_usuario(usuario=user, session=session)
