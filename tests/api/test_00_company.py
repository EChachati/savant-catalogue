import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from core.sql.database import engine
from core.sql.models import Company
from main import app

client = TestClient(app)
BASE_PATH = "/company/"

data = {
    "name": "Savant",
    "phone": "+584121234567",
}


@pytest.fixture(name="get_last_id")
def get_last_id_fixture():
    return (
        Session(engine)
        .exec(select(Company).order_by(Company.id.desc()))
        .first()
        .id
    )


def test_create_company():
    response = client.post(BASE_PATH, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == data["name"]


def test_get_company(get_last_id):
    response = client.get(BASE_PATH + str(get_last_id))
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)
    assert "id" in response.json()
    assert "name" in response.json()
    assert "phone" in response.json()


def test_list_company():
    response = client.get(BASE_PATH)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert isinstance(response.json()[0], dict)
    assert "id" in response.json()[0]
    assert "name" in response.json()[0]


def test_update_company(get_last_id):
    data.update({"name": "TotallyNotSavant", "id": get_last_id})
    response = client.put(BASE_PATH, json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == data["name"]


def test_delete_company(get_last_id):
    response = client.delete(BASE_PATH + str(get_last_id))

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)

    response = client.delete(BASE_PATH + str(999999))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert isinstance(response.json(), dict)
