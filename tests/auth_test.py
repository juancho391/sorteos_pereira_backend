from fastapi import status


def test_register_admin(client):
    response = client.post(
        "/auth/register",
        json={
            "cedula": "1223455667",
            "email": "juan@gmail.com",
            "nombre": "juan bedoya",
            "direccion": "torre 4 apto 1",
            "celular": "3001234567",
            "password": "juan12",
            "is_admin": True,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_login_success(client):
    # Registro el usuario
    client.post(
        "/auth/register",
        json={
            "cedula": "1223455667",
            "email": "juan@gmail.com",
            "nombre": "juan bedoya",
            "direccion": "torre 4 apto 1",
            "celular": "3001234567",
            "password": "juan1234",
            "is_admin": True,
        },
    )
    # Intento de iniciar sesion
    response = client.post(
        "/auth/token", json={"email": "juan@gmail.com", "password": "juan1234"}
    )
    assert response.status_code == status.HTTP_200_OK


def test_login_invalid_credentials(client):
    # Registro el usuario
    client.post(
        "/auth/register",
        json={
            "cedula": "1223455667",
            "email": "juan@gmail.com",
            "nombre": "juan bedoya",
            "direccion": "torre 4 apto 1",
            "celular": "3001234567",
            "password": "juan123",
            "is_admin": True,
        },
    )
    # Intento de iniciar sesion
    response = client.post(
        "/auth/token", json={"email": "juan@gmail.com", "password": "juan12"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
