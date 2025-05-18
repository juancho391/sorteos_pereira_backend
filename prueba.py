import random


def generarNumero(
    lista_numeros: list[int],
    cantidad_numeros: int,
    lista_numeros_especiales: list[int],
    cantidad_comprada: int = 3,
) -> int:
    lista_numeros_generados = []
    contador = 0
    contador_premiados = 0
    verificar = True
    if verificar == False:
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
    return lista_numeros_generados


lista = []
for i in range(0, 9996):
    lista.append(i)

lista_premiados = []
for i in range(0, 20):
    lista_premiados.append(random.randint(1, 9001))
# Deuda tecnica validacion de la cantidad de boletas disponibles
print(
    generarNumero(
        lista_numeros=lista,
        cantidad_numeros=9999,
        lista_numeros_especiales=lista_premiados,
        cantidad_comprada=4,
    )
)
