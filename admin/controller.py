from fastapi import APIRouter


admin_router = APIRouter()


@admin_router.post("/rifa")
def crear_rifa():
    pass
