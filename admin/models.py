from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    cedula: str
    email: EmailStr
    nombre: str
    direccion: str
    celular: str


class UserAdmin(UserResponse):
    is_admin: bool
    password: str
