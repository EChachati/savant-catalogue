from fastapi import APIRouter, status

from core.controllers.purchase import PurchaseController
from core.sql.models import Purchase, PurchaseCreate, PurchaseResponse

router = APIRouter()


@router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=Purchase)
def get_purchase(pk: int):
    return PurchaseController().get(pk)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PurchaseResponse,
)
def create_purchase(purchase: PurchaseCreate):
    return PurchaseController().create(purchase)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Purchase])
def list_companies():
    return PurchaseController().list()


@router.put("/", status_code=status.HTTP_200_OK, response_model=Purchase)
def update_purchase(purchase: Purchase):
    return PurchaseController().update(purchase)


@router.delete("/{pk}", status_code=status.HTTP_200_OK, response_model=Purchase)
def delete_purchase(pk: int):
    return PurchaseController().delete(pk)
