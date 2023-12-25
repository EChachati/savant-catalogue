from collections import Counter

from sqlmodel_crud_manager.crud import CRUDManager

from core.api.product import crud as product_crud
from core.sql.database import engine
from core.sql.models import (
    Purchase,
    PurchaseCreate,
    PurchaseProductLink,
    PurchaseResponse,
)


class PurchaseController:
    def __init__(self):
        self.crud = CRUDManager(Purchase, engine)
        self.product_crud = product_crud

    def get(self, pk: int) -> PurchaseResponse:
        obj = PurchaseResponse.model_validate(self.crud.get(pk))
        obj.total = sum([link.amount for link in obj.product_links])
        return obj

    def create(self, purchase: PurchaseCreate):
        purchase_obj = self.crud.create(purchase)

        product_ids = purchase.product_ids
        products = self.product_crud.get_by_ids(
            product_ids,
            self.crud.db,
        )

        quantities = dict(Counter(purchase.product_ids))

        for product in products:
            self.crud.db.add(
                PurchaseProductLink(
                    purchase_id=purchase_obj.id,
                    product_id=product.id,
                    quantity=quantities[product.id],
                    amount=quantities[product.id] * product.price,
                )
            )
        self.crud.db.commit()
        return self.get(purchase_obj.id)

    def list(self):
        return self.crud.list()

    def update(self, purchase: Purchase):
        return self.crud.update(purchase)

    def delete(self, pk: int):
        return self.crud.delete(pk)
