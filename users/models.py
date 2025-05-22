from sqlmodel import SQLModel


class User(SQLModel):
    id: int
    cedula: str
    email: str
    nombre: str
    direccion: str
    celular: str


class UserCreate(SQLModel):
    nombre: str
    email: str
    celular: str
    direccion: str
    cedula: str
