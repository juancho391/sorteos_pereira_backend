from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class Users(SQLModel, table=True):
    __tablename__ = "Users"
    id: int | None = Field(default=None, primary_key=True)
    cedula: str
    email: EmailStr
    nombre: str
    direccion: str
    celular: str


class UserResponse(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    cedula: str
    email: EmailStr
