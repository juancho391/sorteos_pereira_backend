from sqlmodel import select
from schemas.Boleta_schema import Boleta, BoletaConsulta


class BoletaModel:
    def __init__(self, session):
        self.session = session

    def obtener_boletas_por_rifa(self, id_rifa):
        boletas = self.session.exec(
            select(Boleta).where(Boleta.id_rifa == id_rifa)
        ).all()

        if boletas:
            return boletas
        return None

    def crear_boleta(self, boleta: Boleta):
        self.session.add(boleta)
        self.session.commit()
        self.session.refresh(boleta)
        return boleta

    def obtener_boleta(self, boleta: BoletaConsulta):
        boleta_obtenida = self.session.exec(
            select(Boleta).where(
                Boleta.numero == boleta.numero, Boleta.id_rifa == boleta.id_rifa
            )
        ).first()

        if boleta_obtenida:
            return boleta_obtenida
        return None
