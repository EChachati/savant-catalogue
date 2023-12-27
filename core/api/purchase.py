from fastapi import APIRouter, status

from core.controllers.purchase import PurchaseController
from core.sql.models.purchase import Purchase, PurchaseCreate, PurchaseResponse

router = APIRouter()


@router.get(
    "/{pk}", status_code=status.HTTP_200_OK, response_model=PurchaseResponse
)
def get_purchase(pk: int):
    return PurchaseController().get(pk)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PurchaseResponse,
)
def create_purchase(purchase: PurchaseCreate):
    return PurchaseController().create(purchase)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[PurchaseResponse],
)
def list_purchases():
    return PurchaseController().list()


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PurchaseResponse,
)
def update_purchase(purchase: Purchase):
    return PurchaseController().update(purchase)


@router.delete(
    "/{pk}",
    status_code=status.HTTP_200_OK,
    response_model=PurchaseResponse,
)
def delete_purchase(pk: int):
    return PurchaseController().delete(pk)


@router.get(
    "/message/{pk}",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
def get_purchase_as_message(pk: int):
    return PurchaseController().get_as_message(pk)
