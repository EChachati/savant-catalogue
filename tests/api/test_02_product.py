import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from core.sql.database import engine
from core.sql.models.product import Product
from main import app

client = TestClient(app)
BASE_PATH = "/product/"

data = {
    "name": "Product",
    "description": "Product Test",
    "price": 100.00,
    # "image": "https://inaturalist-open-data.s3.amazonaws.com/photos/166000186/medium.jpg",
    "category_id": 1,
    "company_id": 1,
}


@pytest.fixture(name="get_last_id")
def get_last_id_fixture():
    return (
        Session(engine)
        .exec(select(Product).order_by(Product.id.desc()))
        .first()
        .id
    )


@pytest.fixture(name="create_data")
def test_create_data():
    company = client.post(
        "/company/", json={"name": "Company", "phone": "123456789"}
    ).json()
    category = client.post("/category/", json={"name": "Category"}).json()
    return company.get("id"), category.get("id")


def test_create_product(create_data):
    data.update(
        {
            "category_id": create_data[1],
            "company_id": create_data[0],
        }
    )
    response = client.post(BASE_PATH, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == data["name"]


def test_get_product(get_last_id):
    response = client.get(BASE_PATH + str(get_last_id))
    assert response.status_code == status.HTTP_200_OK


def test_list_product():
    response = client.get(BASE_PATH)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert isinstance(response.json()[0], dict)
    assert "id" in response.json()[0]
    assert "name" in response.json()[0]


def test_update_product(get_last_id):
    data.update({"name": "TotallyNotSavant", "id": get_last_id})
    response = client.put(BASE_PATH, json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == data["name"]


def test_delete_product(get_last_id):
    response = client.delete(BASE_PATH + str(get_last_id))

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)

    response = client.delete(BASE_PATH + str(999999))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert isinstance(response.json(), dict)
