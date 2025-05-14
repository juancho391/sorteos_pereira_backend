from sqlmodel import SQLModel, Field


class Numero_especial(SQLModel, table=True):
    __tablename__ = "Numero_especial"
    id: int | None = Field(default=None, primary_key=True)
    numero: int
    id_rifa: int = Field(foreign_key="Rifa.id")
    disponible: bool | None = Field(default=True)

    def __repr__(self):
        return f"Numero_especial(id={self.id}, numero={self.numero}, id_rifa={self.id_rifa}, disponible={self.disponible})"