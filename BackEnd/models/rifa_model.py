from schemas.Rifa_schema import Rifa
from schemas.Numero_schemna import Numero_especial
from sqlmodel import select


class RifaModel:
    def __init__(self, session):
        self.session = session

    def obtener_rifas(self):
        rifas = self.session.exec(select(Rifa)).all()
        return rifas

    def obtener_rifa(self, id: int):
        rifa = self.session.get(Rifa, id)
        if rifa:
            return rifa
        return None

    def crear_rifa(self, rifa: Rifa):
        self.session.add(rifa)
        self.session.commit()
        self.session.refresh(rifa)
        return rifa

    def finalizar_rifa(self, id: int):
        rifa = self.session.get(Rifa, id)
        if rifa and rifa.is_active == True:
            rifa.is_active = False
            self.session.add(rifa)
            self.session.commit()
            self.session.refresh(rifa)
            return rifa
        return None

    def obtener_rifa_activa(self):
        consulta = select(Rifa).where(Rifa.is_active == True)
        resultado = self.session.exec(consulta)
        rifa = resultado.one_or_none()
        if rifa:
            return rifa
        return None
