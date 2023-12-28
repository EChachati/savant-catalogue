from fastapi import APIRouter, status

from core.controllers.purchase import PurchaseController
from core.sql.models.purchase import Purchase, PurchaseCreate, PurchaseResponse

router = APIRouter()


@router.get(
    "/{pk}",
    status_code=status.HTTP_200_OK,
    response_model=PurchaseResponse,
)
def get_purchase(pk: int):
    """
    The function `get_purchase` retrieves a purchase with a given primary key.

    Arguments:
    * `pk`: The parameter "pk" is an integer that represents the primary key of
    the purchase that we
    want to retrieve.

    Returns:
    the result of the `get()` method from the `PurchaseController` class, which
    is expected to return a
    `PurchaseResponse` object.
    """
    return PurchaseController().get(pk)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PurchaseResponse,
)
def create_purchase(purchase: PurchaseCreate):
    """
    Create a purchase and return it as a JSON

    Args:
        purchase: The PurchaseCreate to create.

    Returns:
        The created purchase.
    """
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
