import random
from typing import Annotated

from fastapi import Depends

from ..boleta.boletaService import boleta_service_dependency
from ..numeros.numeroService import numero_service_dependency
from ..rifa.service import rifa_service_dependency


class GeneradorNumeros:
    def __init__(
        self,
        rifa_service: rifa_service_dependency,
        service_numeros: boleta_service_dependency,
        service_numeros_especiales: numero_service_dependency,
    ):
        self.rifa_service = rifa_service
        self.service_numeros = service_numeros
        self.numeros_especiales_service = service_numeros_especiales

    def generar_numeros(
        self,
        lista_numeros: list[int],
        cantidad_numeros: int,
        lista_numeros_especiales: list[int],
        rifa_id: int,
        cantidad_comprada: int = 3,
    ) -> list[int]:
        numeros_disponibles = cantidad_numeros - len(lista_numeros)
        if numeros_disponibles < cantidad_comprada:
            raise ValueError("No hay suficientes numeros disponibles para la compra")
        lista_numeros_generados = []
        contador = 0
        contador_premiados = 0
        verificar = self.rifa_service.verificar_rifas_activas()
        if verificar:
            raise ValueError("No se pueden generar numeros, hay mas de una rifa activa")
        while contador < cantidad_comprada:
            numero = random.randint(1, cantidad_numeros)
            if numero not in lista_numeros_generados and numero not in lista_numeros:
                if numero in lista_numeros_especiales and contador_premiados < 1:
                    lista_numeros_generados.append(numero)
                    contador_premiados += 1
                    contador += 1
                else:
                    lista_numeros_generados.append(numero)
                    contador += 1

        for numero in lista_numeros_generados:
            if numero in lista_numeros_especiales:
                self.numeros_especiales_service.cambiar_disponibilidad_numero_especial(
                    numero=numero, id_rifa=rifa_id
                )
        return lista_numeros_generados

    def generar_compra_boletas(self, cantidad_comprada: int, id_rifa: int):
        rifa_activa = self.rifa_service.obtener_rifa_id(rifa_id=id_rifa)
        lista_numeros = self.service_numeros.obtener_boletas_vendidas(id_rifa=id_rifa)
        lita_numeros_especiales = self.numeros_especiales_service.obtener_numeros_rifa(
            rifa_activa=rifa_activa
        )
        numeros_generados = self.generar_numeros(
            lista_numeros=lista_numeros,
            cantidad_numeros=9999,
            lista_numeros_especiales=lita_numeros_especiales,
            cantidad_comprada=cantidad_comprada,
            rifa_id=rifa_activa.id,
        )
        return numeros_generados


def get_generador_numeros(
    rifa_service: rifa_service_dependency,
    service_numeros: boleta_service_dependency,
    service_numeros_especiales: numero_service_dependency,
):
    return GeneradorNumeros(
        rifa_service=rifa_service,
        service_numeros=service_numeros,
        service_numeros_especiales=service_numeros_especiales,
    )


generador_numeros_dependency = Annotated[
    GeneradorNumeros, Depends(get_generador_numeros)
]
