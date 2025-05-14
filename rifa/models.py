from pydantic import BaseModel
from schemas.Numero_schemna import Numero_especial
class Rifa(BaseModel):
    id : int
    premio : str
    tipo : str
    is_active : bool
    fecha_inicio : str
    fecha_fin : str
    image_premio : str
    precio : int

    class Config:
        orm_mode = True

class RifaResponse(BaseModel):
    id : int
    premio : str
    tipo : str
    is_active : bool
    fecha_inicio : str
    fecha_fin : str
    image_premio : str
    numeros_especiales : list[Numero_especial]

    class Confgig:
        orm_mode = True