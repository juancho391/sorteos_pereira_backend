from schemas.Rifa_schema import Rifa
from sqlmodel import select


class RifaService:
    def __init__(self, session):
        self.session = session

    def obtener_rifas(self):
        return self.session.excec(select()).all

    def obtener_rifa(self, id: int):
        rifa = self.session.get(Rifa, id)
        if rifa:
            return rifa
        return False

    def crear_rifa(self, rifa: Rifa):
        self.session.add(rifa)
        self.session.commit()
        self.session.refresh(rifa)
        return rifa

    def finalizar_rifa(self, id: int):
        rifa = self.session.get(Rifa, id)
        if rifa:
            rifa.is_active = False
            self.session.add(rifa)
            self.session.commit()
            self.session.refresh(rifa)
            return rifa
        return False
