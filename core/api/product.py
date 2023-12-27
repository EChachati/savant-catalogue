from fastapi import APIRouter, status
from sqlmodel import select
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
def list_products(
    company_id: int | None = None,
    category_id: int | None = None,
):
    query = select(Product)
    if company_id:
        query = query.where(Product.company_id == company_id)
    if category_id:
        query = query.where(Product.category_id == category_id)
    return crud.db.exec(query).all()


@router.put("/", status_code=status.HTTP_200_OK, response_model=Product)
def update_product(product: Product):
    return crud.update(product)


@router.delete("/{pk}", status_code=status.HTTP_200_OK, response_model=Product)
def delete_product(pk: int):
    return crud.delete(pk)
