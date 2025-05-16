from typing import Optional
from sqlmodel import SQLModel


class NumeroEspecialCreate(SQLModel):
    id: Optional[int] = None
    numero: int
    id_rifa: int
    disponible: bool
