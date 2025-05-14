from datetime import date
from pydantic import BaseModel
from typing import Optional


class Numero_especial(BaseModel):
    id: int
    numero: int
    id_rifa: int
    disponible: bool | None = True


class RifaCreate(BaseModel):
    id: Optional[int] = None
    premio: str
    tipo: str
    is_active: Optional[bool] = True
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    image_premio: str
    precio: int


class RifaResponse(BaseModel):
    id : int
    premio : str
    tipo : str
    is_active : bool
    fecha_inicio : date
    fecha_fin : Optional[date] = None
    image_premio : str
    numeros_especiales : Optional[list[Numero_especial]] = None
    precio : int
