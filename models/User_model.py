from schemas.User_schema import Users
from sqlmodel import select


class UserModel:
    def __init__(self, session):
        self.session = session

    def obtener_usuarios(self):
        return self.session.exec(select(Users)).all()

    def crear_usuario(self, user: Users):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def obtener_usuario(self, id: int):
        user = self.session.get(Users, id)
        if user:
            return user
        return None
