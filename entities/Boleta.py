from sqlmodel import SQLModel, Field, Relationship
from .Rifa import Rifa


class Boleta(SQLModel, table=True):
    __tablename__ = "Boleta"
    id: int | None = Field(default=None, primary_key=True)
    id_usuario: int | None = Field(default=None, foreign_key="Users.id")
    id_rifa: int | None = Field(default=None, foreign_key="Rifa.id")
    numero: int

    rifa: Rifa | None = Relationship(back_populates="boletas")
