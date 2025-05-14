from fastapi import APIRouter
from ..db.conexion import session_dependency
from . import models
from . import service


auth_router = APIRouter()


@auth_router.post("/token")
async def login(user: models.USerLogin, session: session_dependency):
    return service.login_usuario(usuario=user, session=session)
