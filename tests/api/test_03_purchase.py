import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from core.sql.database import engine
from core.sql.models.purchase import Purchase
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
        "/company/", json={"name": "Company", "phone": "+584123456789"}
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
    return company.get("id"), product.get("id")


def test_create_purchase(create_data):
    data.update(
        {"company_id": create_data[0], "product_ids": [create_data[1]] * 10}
    )
    response = client.post(BASE_PATH, json=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.json(), dict)
    assert "id" in response.json()
    assert "company_id" in response.json()
    assert "products_purchased" in response.json()
    assert "total" in response.json()
    assert isinstance(response.json()["products_purchased"], list)
    assert isinstance(response.json()["products_purchased"][0], dict)
    assert "product_id" in response.json()["products_purchased"][0]
    assert "quantity" in response.json()["products_purchased"][0]
    assert "amount" in response.json()["products_purchased"][0]


def test_get_purchase(get_last_id):
    response = client.get(BASE_PATH + str(get_last_id))
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)
    assert "id" in response.json()
    assert "company_id" in response.json()
    assert "products_purchased" in response.json()
    assert "total" in response.json()
    assert isinstance(response.json()["products_purchased"], list)
    assert isinstance(response.json()["products_purchased"][0], dict)
    assert "product_id" in response.json()["products_purchased"][0]
    assert "quantity" in response.json()["products_purchased"][0]
    assert "amount" in response.json()["products_purchased"][0]


def test_list_purchase():
    response = client.get(BASE_PATH)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert isinstance(response.json()[0], dict)
    assert "id" in response.json()[0]
    assert "company_id" in response.json()[0]
    assert "products_purchased" in response.json()[0]
    assert "total" in response.json()[0]
    assert isinstance(response.json()[0]["products_purchased"], list)
    assert isinstance(response.json()[0]["products_purchased"][0], dict)
    assert "product_id" in response.json()[0]["products_purchased"][0]
    assert "quantity" in response.json()[0]["products_purchased"][0]
    assert "amount" in response.json()[0]["products_purchased"][0]
