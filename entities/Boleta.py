from sqlmodel import SQLModel, Field
from .Rifa import Rifa
from .User import Users


class Boleta(SQLModel, table=True):
    __tablename__ = "Boleta"
    id: int | None = Field(default=None, primary_key=True)
    id_usuario: int | None = Field(default=None, foreign_key="Users.id")
    id_rifa: int | None = Field(default=None, foreign_key="Rifa.id")
    numero: int
    disponible: bool | None = True


class BoletaConsulta(SQLModel):
    numero: int
    id_rifa: int
