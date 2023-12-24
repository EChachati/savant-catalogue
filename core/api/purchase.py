from fastapi import APIRouter, status
from sqlmodel_crud_manager.crud import CRUDManager

from core.sql.database import engine as db_engine
from core.sql.models import Purchase, PurchaseCreate

router = APIRouter()

crud = CRUDManager(Purchase, db_engine)


@router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=Purchase)
def get_purchase(pk: int):
    return crud.get(pk)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Purchase)
def create_purchase(purchase: PurchaseCreate):
    return crud.create(purchase)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Purchase])
def list_companies():
    return crud.list()


@router.put("/", status_code=status.HTTP_200_OK, response_model=Purchase)
def update_purchase(purchase: Purchase):
    return crud.update(purchase)


@router.delete("/{pk}", status_code=status.HTTP_200_OK, response_model=Purchase)
def delete_purchase(pk: int):
    return crud.delete(pk)
