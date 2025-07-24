from fastapi import FastAPI

from .auth.controller import auth_router
from .compra.controller import router_compra
from .numeros.controller import router_numeros
from .rifa.controller import router_rifa


def registrar_routers(app: FastAPI):
    app.include_router(auth_router, prefix="/auth")
    app.include_router(router_rifa, prefix="/rifa")
    app.include_router(router_numeros, prefix="/numeros")
    app.include_router(router_compra, prefix="/compra")
