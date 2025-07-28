import io


def get_token(client):
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
    return response.json().get("access_token")


def test_rifa_create(client):
    token = get_token(client)
    data = {
        "premio": "Ford Mustang",
        "tipo": "Carro",
        "precio": 10000,
    }

    fake_image = io.BytesIO(b"fake image content")
    files = {
        "image": ("test.jpg", fake_image, "image/jpeg"),
    }
    response = client.post(
        "/rifa/",
        data=data,
        headers={"Authorization": f"Bearer {token}"},
        files=files,
    )
    assert response.status_code == 200


def test_get_rifa_activa(client):
    # Primero, crear una rifa para que exista una activa
    token = get_token(client)
    data = {
        "premio": "Ford Mustang",
        "tipo": "Carro",
        "precio": 10000,
    }

    fake_image = io.BytesIO(b"fake image content")
    files = {
        "image": ("test.jpg", fake_image, "image/jpeg"),
    }
    response = client.post(
        "/rifa/",
        data=data,
        headers={"Authorization": f"Bearer {token}"},
        files=files,
    )
    assert response.status_code == 200
    response_read = client.get(
        "/rifa/activa",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_read.status_code == 200
    assert response_read.json()["premio"] == "Ford Mustang"
