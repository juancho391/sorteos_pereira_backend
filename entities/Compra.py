from sqlmodel import SQLModel, Field
from .User import Users
from pydantic import EmailStr
from .Rifa import Rifa


class Compra(SQLModel, table=True):
    __tablename__ = "Compra"
    id: int | None = Field(default=None, primary_key=True)
    id_rifa: int = Field(foreign_key="Rifa.id")
    id_usuario: int = Field(foreign_key="Users.id")
    cantidad: int
    total: int
