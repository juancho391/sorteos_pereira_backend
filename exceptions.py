from fastapi import HTTPException


# Excepcion de error de usuario base
class UserError(HTTPException):
    pass


# Excepcion de usuario no encontrado
class UserNotFoundError(UserError):
    def __init__(self, usuario_id):
        mensaje = (
            "Usuario no encontrado"
            if usuario_id is None
            else f"Usuario con id {usuario_id} no encontrado"
        )
        super().__init__(status_code=404, detail=mensaje)


class UserCreationError(HTTPException):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Fallo al crear el usuario: {error}")


# Excepcion de autenticacion de usuario
class AuthenticationError(HTTPException):
    def __init__(self, mensaje: str = "No se pudo validar el usuario"):
        super().__init__(status_code=401, detail=mensaje)


class RifaCreationError(HTTPException):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Fallo al crear la rifa: {error}")


class RifaIDNotFoundError(HTTPException):
    def __init__(self, id: int):
        super().__init__(status_code=404, detail=f"No se encontro la rifa con id {id}")


class RifasNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="No se encontraron rifas")


class NumeroEspecialCreationError(HTTPException):
    def __init__(self, error: str):
        super().__init__(
            status_code=500, detail=f"Fallo al crear el numero especial: {error}"
        )


class NumeroEspecialNotFoundError(HTTPException):
    def __init__(self, id: int):
        super().__init__(
            status_code=404, detail=f"No se encontro el numero especial con id:  {id}"
        )


class NumerosEspecialesNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="No se encontraron numeros especiales")


class NumeroEspecialDeleteError(HTTPException):
    def __init__(self, error: str):
        super().__init__(
            status_code=500, detail=f"Fallo al eliminar el numero especial: {error}"
        )


class BoletaNotFoundError(HTTPException):
    def __init__(self, numero: int):
        super().__init__(status_code=404, detail=f"No se encontro la boleta: {numero}")


class BoletasCreationError(HTTPException):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Fallo al crear las boletas: {error}")


class RifaNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="No se encontro rifa activa")


class CompraCreationError(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="Fallo al crear la compra")
