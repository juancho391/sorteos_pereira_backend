from fastapi import APIRouter
from ..db.conexion import session_dependency
from . import models
from . import service
from ..entities.User import UserAdminCreate, UserResponse


auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/token")
async def login(user: models.USerLogin, session: session_dependency):
    return service.login_usuario(usuario=user, session=session)


@auth_router.post("/register", response_model=UserResponse)
async def register(user: UserAdminCreate, session: session_dependency):
    return service.registrar_usuario(usuario=user, session=session)
