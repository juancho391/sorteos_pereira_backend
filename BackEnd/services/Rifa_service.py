from models.rifa_model import RifaModel
from schemas.Rifa_schema import Rifa
from schemas.Numero_schemna import Numero_especial
from models.numero_model import NumeroModel
from models.Boleta_model import BoletaModel
from models.User_model import UserModel
from schemas.Boleta_schema import BoletaConsulta


class RifaService:
    def __init__(self, session):
        self.session = session
        self.boleta_model = BoletaModel(session=self.session)
        self.user_model = UserModel(session=self.session)

    def obtener_rifas(self):
        rifas = RifaModel(session=self.session).obtener_rifas()
        if not rifas:
            raise ValueError("No se encontraron rifas")
        return rifas

    def obtener_rifa(self, id: int):
        rifa = RifaModel(session=self.session).obtener_rifa(id=id)
        if not rifa:
            raise ValueError(f"No se encontro la rifa con id{id}")
        return rifa

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

    def agregar_numero_especial(self, numero_especial: Numero_especial):
        id_rifa = numero_especial.id_rifa
        rifa = RifaModel(session=self.session).obtener_rifa(id=id_rifa)
        # Validamos que exista la rifa y este activa
        if not rifa or rifa.is_active == False:
            raise ValueError(
                f"No se pudo agregar el numero especial a la rifa con id : {id_rifa}"
            )
        # Consultamos los numeros especiales que pertenecen a la rifa
        numeros_especiales = NumeroModel(
            session=self.session
        ).obtener_numeros_especiales(id_rifa=id_rifa)
        # Validamos que la rifa no tenga un numero especial con el mismo numero
        for numero in numeros_especiales:
            if numero.numero == numero_especial.numero:
                raise ValueError(
                    f"Ya existe un numero especial con el numero {numero_especial.numero}"
                )
        numero_creado = NumeroModel(session=self.session).crear_numero(numero_especial)
        return numero_creado

    def obtener_ganador(self, boleta: BoletaConsulta):
        # primero verifico que la boleta exista
        boleta_obtenida = self.boleta_model.obtener_boleta(boleta=boleta)
        if not boleta_obtenida:
            raise ValueError(
                f"No se encontro la boleta con el numero {boleta.numero} y rifa {boleta.id_rifa}"
            )
        # busco el usuario al que pertenece la boleta
        usuario = self.user_model.obtener_usuario(id=boleta_obtenida.id_usuario)
        if usuario:
            return usuario

        raise ValueError(
            f"No se encontro el usuario con el id {boleta_obtenida.id_usuario}"
        )
