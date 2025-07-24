from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class Users(SQLModel, table=True):
    __tablename__ = "Users"
    id: int | None = Field(default=None, primary_key=True)
    cedula: str = Field(unique=True)
    email: EmailStr = Field(unique=True, index=True)
    nombre: str
    direccion: str
    celular: str
    is_admin: bool | None = Field(default=False)
    password: str | None = Field(default=None)


class UserCreate(SQLModel):
    cedula: str
    email: EmailStr
    nombre: str
    direccion: str
    celular: str


class UserResponse(UserCreate):
    id: int


class UserAdminCreate(UserCreate):
    password: str
    is_admin: bool | None = True
