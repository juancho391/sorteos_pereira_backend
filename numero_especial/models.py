from pydantic import BaseModel
from typing import Optional


class NumeroEspecialCreate(BaseModel):
    id: Optional[int] = None
    numero: int
    id_rifa: int
    disponible: bool
