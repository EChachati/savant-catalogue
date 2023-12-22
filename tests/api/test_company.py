from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
BASE_PATH = "/company/"

path = {
    "get": BASE_PATH + "1",
    "create": BASE_PATH,
    "list": BASE_PATH,
    "update": BASE_PATH,
    "delete": BASE_PATH + "1",
}

data = {
    "name": "Savant",
    "phone": "+584121234567",
}


def test_create_company():
    response = client.post(path["create"], json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == data["name"]


def test_get_company():
    response = client.get(path["get"])
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1


def test_list_company():
    response = client.get(path["list"])
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert isinstance(response.json()[0], dict)
    assert "id" in response.json()[0]
    assert "name" in response.json()[0]


def test_update_company():
    data.update({"name": "TotallyNotSavant"})
    response = client.put(path["update"], json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == data["name"]


def test_delete_company():
    response = client.delete(path["delete"])

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)

    path.update({"delete": BASE_PATH + "99999"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert isinstance(response.json(), dict)
