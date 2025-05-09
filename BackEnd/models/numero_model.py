from schemas.Numero_schemna import Numero_especial
from sqlmodel import select


class NumeroModel:
    def __init__(self, session):
        self.session = session

    def crear_numero(self, numero: Numero_especial):
        self.session.add(numero)
        self.session.commit()
        self.session.refresh(numero)
        return numero

    def obtener_numeros_especiales(self, id_rifa: int):
        numeros = self.session.exec(
            select(Numero_especial).where(Numero_especial.id_rifa == id_rifa)
        ).all()

        return numeros
