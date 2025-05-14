from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import time, date
from schemas.Numero_schemna import Numero_especial

# Clase para crear la tabla
class Rifa(SQLModel, table=True):
    __tablename__ = "Rifa"
    id: int | None = Field(default=None, primary_key=True)
    premio: str
    tipo: str
    is_active: bool | None = Field(default=True)
    fecha_inicio: Optional[date] = Field(default=date.today())
    fecha_fin: Optional[date] = Field(default=None)
    image_premio: str


class RifaResponse(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    premio: str
    tipo: str
    is_active: bool | None = Field(default=True)
    fecha_inicio: Optional[date] = Field(default=date.today())
    fecha_fin: Optional[date] = Field(default=None)
    image_premio: str
    numeros_especiales: list[Numero_especial] | None = None
