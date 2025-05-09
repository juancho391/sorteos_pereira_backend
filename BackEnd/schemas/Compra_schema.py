from sqlmodel import SQLModel
from .User_schema import Users
from pydantic import EmailStr
from schemas.User_schema import UserResponse


class Compra(SQLModel):
    usuario: UserResponse
    id_rifa: int
    precio_boleta: int
    cantidad: int
    total: int
