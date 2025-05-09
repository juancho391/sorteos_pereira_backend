from schemas.Rifa_schema import Rifa


class RifaService:
    def __init__(self, session):
        self.session = session

    def crear_rifa(self, rifa: Rifa):
        self.session.add(rifa)
        self.session.commit()
        self.session.refresh(rifa)
        return rifa
