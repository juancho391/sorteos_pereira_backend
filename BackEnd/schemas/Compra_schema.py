from sqlmodel import SQLModel
from .User_schema import Users
from pydantic import EmailStr
from schemas.User_schema import Users


class Compra(SQLModel):
    usuario: Users
    precio_boleta: int
    cantidad: int
    total: int
