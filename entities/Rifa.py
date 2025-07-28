from datetime import date
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


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
    precio: int

    numeros_especiales: list["NumeroEspecial"] = Relationship(back_populates="rifa")
    boletas: list["Boleta"] = Relationship(back_populates="rifa")
