from sqlmodel import SQLModel


class BoletaCreate(SQLModel):
    id_usuario: int
    numero: int
    id_rifa: int
