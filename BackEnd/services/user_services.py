from schemas import User_schema
from models import User_model
from typing import Optional

class User_services:
    def __init__(self, session):
        # Session para hacer las consultas
        self.session = session
        # Instancia del usuario modelo para hacer consultas
        self.user_model = User_model.User_model(session=session)

    def crear_user(self, user: User_schema.Users):
        # Si el 
        if self.user_model.obtener_user(user=user):
            raise ValueError("El usuario ya existe")
        else:
            usuario_creado = self.user_model.crear_usuario(user=user)
            usuario_creado_response = User_schema.UserResponse(
                nombre= usuario_creado.nombre,
                email= usuario_creado.email,
                cedula= usuario_creado.cedula,
                celular= usuario_creado.celular,
                direccion= usuario_creado.direccion
                )
            return usuario_creado_response

    def login_user(self, user_admin: User_schema.UserAdminLogin):
        user_posible = self.user_model.obtener_user(user_admin)
        if not user_posible:
            raise ValueError("El usuario no existe")
        elif not self.user_model.validar_contraseña(user_admin=user_admin, user_posible=user_posible):
            raise ValueError("Las contraseñas no coinciden")
        else:
            return user_posible
            
