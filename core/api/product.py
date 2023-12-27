from fastapi import APIRouter, status
from sqlmodel_crud_manager.crud import CRUDManager

from core.sql.database import engine as db_engine
from core.sql.models.product import Product, ProductCreate

router = APIRouter()

crud = CRUDManager(Product, db_engine)


@router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=Product)
def get_product(pk: int):
    return crud.get(pk)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Product)
def create_product(product: ProductCreate):
    return crud.create(product)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Product])
def list_companies():
    return crud.list()


@router.put("/", status_code=status.HTTP_200_OK, response_model=Product)
def update_product(product: Product):
    return crud.update(product)


@router.delete("/{pk}", status_code=status.HTTP_200_OK, response_model=Product)
def delete_product(pk: int):
    return crud.delete(pk)
