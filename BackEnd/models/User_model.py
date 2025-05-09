from schemas.User_schema import Users
from sqlmodel import select


class User_Services:
    def __init__(self, session):
        self.session = session

    def obtener_usuarios(self):
        return self.session.exec(select(Users)).all()

    def crear_usuario(self, user: Users):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
