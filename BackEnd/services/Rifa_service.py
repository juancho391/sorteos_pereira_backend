from models.rifa_model import RifaModel
from schemas.Rifa_schema import Rifa


class RifaService:
    def __init__(self, session):
        self.session = session

    def obtener_rifas(self):
        rifas = RifaModel(session=self.session).obtener_rifas()

        if not rifas:
            raise ValueError("No se encontraron rifas")

        return rifas

    def obtener_rifa(self, id: int):
        pass

    def crear_rifa(self, rifa: Rifa):
        nueva_rifa = RifaModel(session=self.session).crear_rifa(rifa=rifa)

        if not nueva_rifa:
            raise ValueError("No se pudo crear la rifa")

        return nueva_rifa

    def finalizar_rifa(self, id: int):
        rifa = RifaModel(session=self.session).finalizar_rifa(id=id)

        if not rifa:
            raise ValueError("No se pudo finalizar la rifa")

        return rifa
