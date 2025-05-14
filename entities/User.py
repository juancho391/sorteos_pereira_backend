from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class Users(SQLModel, table=True):
    __tablename__ = "Users"
    id: int | None = Field(default=None, primary_key=True)
    cedula: str = Field(unique=True)
    email: EmailStr = Field(unique=True)
    nombre: str
    direccion: str
    celular: str
    is_admin: bool | None = Field(default=False)
    password: str | None = Field(default=None)


class UserAdminLogin(SQLModel):
    email: EmailStr
    password: str


class UserResponse(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    cedula: str
    email: EmailStr
    nombre: str
    direccion: str
    celular: str
