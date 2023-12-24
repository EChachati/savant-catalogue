import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from core.sql.database import engine
from core.sql.models import Purchase
from main import app

client = TestClient(app)
BASE_PATH = "/purchase/"

data = {
    "company_id": 1,
}


@pytest.fixture(name="get_last_id")
def get_last_id_fixture():
    return (
        Session(engine)
        .exec(select(Purchase).order_by(Purchase.id.desc()))
        .first()
        .id
    )


@pytest.fixture(name="create_data")
def test_create_data():
    company = client.post(
        "/company/", json={"name": "Company", "phone": "123456789"}
    ).json()
    category = client.post("/category/", json={"name": "Category"}).json()
    product = client.post(
        "/product/",
        json={
            "name": "Product",
            "description": "Product Test",
            "price": 100.00,
            "image": "https://inaturalist-open-data.s3.amazonaws.com/photos/166000186/medium.jpg",
            "category_id": category.get("id"),
            "company_id": company.get("id"),
        },
    ).json()
    return company.get("id"), category.get("id"), product.get("id")


def test_create_purchase(create_data):
    data.update(
        {
            "company_id": create_data[0],
            "product_id": create_data[2],
            "amount": 100.00,
        }
    )
    response = client.post(BASE_PATH, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == data["name"]


def test_get_purchase(get_last_id):
    response = client.get(BASE_PATH + str(get_last_id))
    assert response.status_code == status.HTTP_200_OK


def test_list_purchase():
    response = client.get(BASE_PATH)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert isinstance(response.json()[0], dict)
    assert "id" in response.json()[0]
    assert "name" in response.json()[0]


def test_update_purchase(get_last_id):
    data.update({"name": "TotallyNotSavant", "id": get_last_id})
    response = client.put(BASE_PATH, json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == data["name"]


def test_delete_purchase(get_last_id):
    response = client.delete(BASE_PATH + str(get_last_id))

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)

    response = client.delete(BASE_PATH + str(999999))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert isinstance(response.json(), dict)
