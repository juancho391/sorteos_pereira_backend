from fastapi import FastAPI
from .auth.controller import auth_router
from .rifa.controller import router_rifa
from .numero_especial.controller import router_numero_especial


def registrar_routers(app: FastAPI):
    app.include_router(auth_router, prefix="/auth")
    app.include_router(router_rifa, prefix="/rifa")
    app.include_router(router_numero_especial, prefix="/numero_especial")
