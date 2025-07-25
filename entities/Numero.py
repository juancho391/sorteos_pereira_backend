from sqlmodel import Field, Relationship, SQLModel

from .Rifa import Rifa


class NumeroEspecial(SQLModel, table=True):
    __tablename__ = "Numero_especial"
    id: int | None = Field(default=None, primary_key=True)
    numero: int
    id_rifa: int = Field(foreign_key="Rifa.id")
    disponible: bool | None = Field(default=True)

    rifa: Rifa | None = Relationship(back_populates="numeros_especiales")
