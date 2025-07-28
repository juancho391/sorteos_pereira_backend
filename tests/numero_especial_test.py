from fastapi import status


def test_create_especial_number(client):
    response = client.post(
        "/numeros/numero_especial",
        json={"numero": 1234, "id_rifa": 1, "disponible": True},
    )
    assert response.status_code == status.HTTP_200_OK
