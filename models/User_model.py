from schemas import User_schema
from sqlmodel import select
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User_model:
    def __init__(self, session):
        self.session = session

    def obtener_usuarios(self):
        return self.session.exec(select(User_schema.Users)).all()

    def obtener_user(self, user_admin: User_schema.Users):
        query = select(User_schema.Users).where(
            User_schema.Users.email == user_admin.email
        )
        user_encontrado = self.session.exec(query).one_or_none()
        return user_encontrado if user_encontrado is not None else False

    def obtener_usuario_id(self, id: int):
        query = select(User_schema.Users).where(User_schema.Users.id == id)
        user_encontrado = self.session.exec(query).one_or_none()
        return user_encontrado if user_encontrado is not None else False

    def crear_usuario(self, user: User_schema.Users):
        if user.is_admin is True:
            user.password = pwd_context.hash(user.password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def validar_contraseña(
        self, user_admin: User_schema.UserAdminLogin, user_posible: User_schema.Users
    ):
        if pwd_context.verify(user_admin.password, user_posible.password):
            return True
        else:
            raise ValueError("Las contraseñas no coinciden")
